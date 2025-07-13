# backend/core/rag_cag_pipeline.py
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from core.config import settings
import requests
import os
import shutil

class RAGCAGPipeline:
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        self.ollama_connected = False
        self.chroma_db_path = settings.CHROMADB_PATH

    async def initialize(self):
        """Initializes Ollama connection, embeddings, and ChromaDB."""
        await self._test_ollama_connection()
        if not self.ollama_connected:
            raise ConnectionError("Failed to connect to Ollama. Please ensure it's running and the model is pulled.")

        self.llm = Ollama(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL, temperature=0.1)
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
        self._init_chroma()
        self._setup_qa_chain()

    async def _test_ollama_connection(self):
        """Tests connection to the Ollama instance."""
        print(f"Attempting to connect to Ollama at {settings.OLLAMA_BASE_URL}...")
        try:
            response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/version", timeout=5)
            response.raise_for_status()
            self.ollama_connected = True
            print(f"Successfully connected to Ollama: {response.json()}")

            # Check if the model is available
            model_list_response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
            model_list_response.raise_for_status()
            models = [m['name'] for m in model_list_response.json().get('models', [])]
            if f"{settings.OLLAMA_MODEL}:latest" not in models and settings.OLLAMA_MODEL not in models:
                print(f"WARNING: Model '{settings.OLLAMA_MODEL}' not found in Ollama. Please pull it using 'ollama pull {settings.OLLAMA_MODEL}'.")
                self.ollama_connected = False # Treat as not connected if model is missing
            else:
                print(f"Model '{settings.OLLAMA_MODEL}' found in Ollama.")

        except requests.exceptions.ConnectionError:
            print(f"ERROR: Could not connect to Ollama at {settings.OLLAMA_BASE_URL}. Is Ollama running?")
            self.ollama_connected = False
        except requests.exceptions.Timeout:
            print(f"ERROR: Connection to Ollama timed out at {settings.OLLAMA_BASE_URL}.")
            self.ollama_connected = False
        except requests.exceptions.RequestException as e:
            print(f"ERROR: An error occurred while connecting to Ollama: {e}")
            self.ollama_connected = False

    def _init_chroma(self):
        """Initializes ChromaDB, creating it if it doesn't exist."""
        # Check if the ChromaDB directory exists and has content
        if os.path.exists(self.chroma_db_path) and os.listdir(self.chroma_db_path):
            print(f"Loading existing ChromaDB from {self.chroma_db_path}")
            self.vectorstore = Chroma(
                persist_directory=self.chroma_db_path,
                embedding_function=self.embeddings
            )
        else:
            print(f"ChromaDB not found or empty at {self.chroma_db_path}. A new one will be created upon ingestion.")
            # Create an empty persistent client for now, data will be added later
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.chroma_db_path
            )
            # Ensure the directory exists
            os.makedirs(self.chroma_db_path, exist_ok=True)
        
        self.vectorstore.persist() # Explicitly persist to ensure directory is set up

    def is_chroma_initialized(self) -> bool:
        """Checks if ChromaDB has any collections (i.e., data ingested)."""
        # A more robust check might involve querying for collections
        # For simplicity, we assume if the directory exists and has files, it's initialized.
        return os.path.exists(self.chroma_db_path) and bool(os.listdir(self.chroma_db_path))

    def ingest_data(self, data: list[dict], data_type: str):
        """
        Ingests data into ChromaDB.
        Assumes data is a list of dicts, and each dict will be converted to a Document.
        """
        if not self.embeddings:
            raise RuntimeError("Embeddings not initialized. Call initialize() first.")
        if not self.vectorstore:
            self._init_chroma() # Ensure vectorstore is ready

        documents = []
        for item in data:
            if data_type == "patient_records":
                content = f"Patient ID: {item.get('id')}\nName: {item.get('name')}\nAge: {item.get('age')}\nDiagnosis: {item.get('diagnosis')}\nMedications: {item.get('medications')}\nHistory: {item.get('history')}\nNotes: {item.get('notes')}"
                metadata = {"source": "patient_records", "id": item.get('id')}
            elif data_type == "treatment_guides":
                content = f"Condition: {item.get('condition')}\nGuide: {item.get('guide')}"
                metadata = {"source": "treatment_guides", "condition": item.get('condition')}
            elif data_type == "drug_interactions":
                content = f"Drug 1: {item.get('drug1')}\nDrug 2: {item.get('drug2')}\nInteraction: {item.get('interaction')}"
                metadata = {"source": "drug_interactions", "drug1": item.get('drug1'), "drug2": item.get('drug2')}
            else:
                continue # Skip unknown data types

            documents.append(Document(page_content=content, metadata=metadata))

        if documents:
            # Using a text splitter for potentially large documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_documents = text_splitter.split_documents(documents)
            
            print(f"Adding {len(split_documents)} documents from {data_type} to ChromaDB...")
            self.vectorstore.add_documents(split_documents)
            self.vectorstore.persist()
            print(f"Successfully ingested {len(split_documents)} documents for {data_type}.")
        else:
            print(f"No documents to ingest for {data_type}.")

    def _setup_qa_chain(self):
        """Sets up the LangChain QA chain for RAG and prepares for CAG."""
        if not self.vectorstore or not self.llm:
            raise RuntimeError("Vectorstore or LLM not initialized. Call initialize() first.")

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        # Prompt for RAG/CAG
        # The prompt is designed to instruct the LLM to use the provided context
        # and to act as a healthcare assistant.
        # It encourages comprehensive and accurate responses,
        # which is key for both RAG (initial retrieval) and CAG (follow-up context).
        prompt_template = """
        You are an AI-powered healthcare assistant for doctors. Your goal is to provide comprehensive, accurate, and relevant medical information based on the provided context.
        The context includes patient records, treatment guides, and drug interaction information.

        Answer the question thoroughly and professionally. If the information is not explicitly available in the provided context, state that clearly.
        Do not make up information.

        Context:
        {context}

        Question: {question}

        Comprehensive Answer:
        """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # RAG part: Retrieve and combine with question
        # For CAG, we rely on the LLM's long context window.
        # Subsequent queries will ideally bring in new relevant docs via retriever,
        # and the LLM itself will manage the accumulating context of the conversation.
        self.qa_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | PROMPT
            | self.llm
            | StrOutputParser()
        )

    async def process_query(self, query: str) -> tuple[str, list[dict]]:
        """
        Processes a natural language query using the RAG/CAG pipeline.
        Returns the generated response and the source documents.
        """
        if not self.qa_chain:
            raise RuntimeError("QA chain not initialized. Call initialize() first.")

        # LangChain's RetrievalQA or custom chain can handle context.
        # For follow-up questions, the entire conversation history (or a summarized version)
        # combined with new retrievals would be passed to the LLM.
        # In this basic setup, the `retriever` fetches new context for each query,
        # and the prompt implicitly expects the LLM to manage its internal conversation state
        # if the LLM itself supports long context.
        # A more advanced CAG would involve explicit conversation history management and summarization.

        # To get source documents, we need to manually run retriever and then the chain
        retrieved_docs = self.retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Prepare source documents for the frontend
        source_docs_for_frontend = [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in retrieved_docs
        ]

        # Use the LangChain Runnable for streamlined execution
        response = self.qa_chain.invoke({"context": context, "question": query})

        return response, source_docs_for_frontend
