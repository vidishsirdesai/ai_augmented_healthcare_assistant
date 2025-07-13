# src/core/rag_cag_pipeline.py
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.core.config import settings
import requests
import os

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
        """Initializes Ollama connection. Embeddings and ChromaDB will be lazily initialized."""
        await self._test_ollama_connection()
        if not self.ollama_connected:
            raise ConnectionError("Failed to connect to Ollama. Please ensure it's running and the model is pulled.")

        # Only initialize LLM here. Embeddings and Vectorstore will be initialized on demand.
        self.llm = Ollama(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL, temperature=0.1)


    async def _test_ollama_connection(self):
        """Tests connection to the Ollama instance."""
        print(f"Attempting to connect to Ollama at {settings.OLLAMA_BASE_URL}...")
        try:
            response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/version", timeout=5)
            response.raise_for_status()
            self.ollama_connected = True
            print(f"Successfully connected to Ollama: {response.json()}")

            model_list_response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
            model_list_response.raise_for_status()
            models = [m['name'] for m in model_list_response.json().get('models', [])]
            if f"{settings.OLLAMA_MODEL}:latest" not in models and settings.OLLAMA_MODEL not in models:
                print(f"WARNING: Model '{settings.OLLAMA_MODEL}' not found in Ollama. Please pull it using 'ollama pull {settings.OLLAMA_MODEL}'.")
                self.ollama_connected = False
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

    def _ensure_embeddings_and_vectorstore(self):
        """Ensures embeddings and vectorstore are initialized. Called by methods that need them."""
        if self.embeddings is None:
            print(f"Initializing HuggingFaceEmbeddings with model: {settings.EMBEDDING_MODEL_NAME}")
            self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)

        if self.vectorstore is None:
            print(f"Initializing ChromaDB client instance at {self.chroma_db_path}")
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.chroma_db_path
            )
            os.makedirs(self.chroma_db_path, exist_ok=True)
            # No explicit persist() needed for Chroma 0.4.x+ on initial client creation

    def is_chroma_initialized_and_populated(self) -> bool:
        """Checks if ChromaDB client is initialized and contains documents."""
        # Ensure client is initialized before checking population
        self._ensure_embeddings_and_vectorstore()

        try:
            collection = self.vectorstore._client.get_or_create_collection(name="langchain")
            if collection.count() > 0:
                print(f"ChromaDB at {self.chroma_db_path} contains {collection.count()} documents.")
                return True
            else:
                print(f"ChromaDB at {self.chroma_db_path} is initialized but appears empty.")
                return False
        except Exception as e:
            print(f"Error checking ChromaDB population: {e}. Assuming empty for now.")
            return False


    def ingest_data(self, data: list[dict], data_type: str):
        """
        Ingests data into ChromaDB.
        Assumes data is a list of dicts, and each dict will be converted to a Document.
        """
        # Ensure embeddings and vectorstore are ready before proceeding
        self._ensure_embeddings_and_vectorstore()

        documents = []
        documents = []
        for item in data:
            content = "" # Initialize content as a string
            metadata = {}

            if data_type == "patient_records":
                # Ensure all parts of content are strings
                content = (
                    f"Patient ID: {item.get('id', 'N/A')}\n"
                    f"Name: {item.get('name', 'N/A')}\n"
                    f"Age: {item.get('age', 'N/A')}\n"
                    f"Diagnosis: {item.get('diagnosis', 'N/A')}\n"
                    f"Medications: {item.get('medications', 'N/A')}\n" # This could be a list/dict
                    f"History: {item.get('history', 'N/A')}\n"
                    f"Notes: {item.get('notes', 'N/A')}"
                )
                metadata = {"source": "patient_records", "id": item.get('id')}
            elif data_type == "treatment_guides":
                content = (
                    f"Condition: {item.get('condition', 'N/A')}\n"
                    f"Guide: {item.get('guide', 'N/A')}"
                )
                metadata = {"source": "treatment_guides", "condition": item.get('condition')}
            elif data_type == "drug_interactions":
                content = (
                    f"Drug 1: {item.get('drug1', 'N/A')}\n"
                    f"Drug 2: {item.get('drug2', 'N/A')}\n"
                    f"Interaction: {item.get('interaction', 'N/A')}" # This could be a list/dict
                )
                metadata = {"source": "drug_interactions", "drug1": item.get('drug1'), "drug2": item.get('drug2')}
            else:
                continue # Skip unknown data types

            # Ensure content is always a string before creating Document
            if not isinstance(content, str):
                print(f"Warning: Document content for {data_type} is not a string. Converting. Content: {content}")
                content = str(content) # Force conversion to string

            documents.append(Document(page_content=content, metadata=metadata))

        if documents:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_documents = text_splitter.split_documents(documents)

            print(f"Adding {len(split_documents)} documents from {data_type} to ChromaDB...")
            self.vectorstore.add_documents(split_documents)
            # No explicit persist() needed for Chroma 0.4.x+ for adding documents
            print(f"Successfully ingested {len(split_documents)} documents for {data_type}.")
        else:
            print(f"No documents to ingest for {data_type}.")

    def _setup_qa_chain(self):
        """Sets up the LangChain QA chain for RAG and prepares for CAG."""
        # Ensure everything needed for the QA chain is initialized and populated
        self._ensure_embeddings_and_vectorstore()
        if not self.llm:
             raise RuntimeError("LLM not initialized when trying to setup QA chain.")
        
        # This check is crucial: only set up if vectorstore has docs to retrieve from.
        if not self.is_chroma_initialized_and_populated():
            raise RuntimeError("Cannot setup QA chain: Vectorstore is not populated with documents.")

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

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

        self.qa_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | PROMPT
            | self.llm
            | StrOutputParser()
        )
        print("QA chain setup complete.")

    async def process_query(self, query: str) -> tuple[str, list[dict]]:
        """
        Processes a natural language query using the RAG/CAG pipeline.
        Returns the generated response and the source documents.
        """
        # Ensure QA chain is set up before processing queries
        if not self.qa_chain:
            # If QA chain is not set up, try to set it up now
            try:
                self._setup_qa_chain()
            except RuntimeError as e:
                # If setup still fails, return an informative message
                return f"The knowledge base is not yet fully ready for queries: {e}", []

        retrieved_docs = self.retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        source_docs_for_frontend = [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in retrieved_docs
        ]

        response = self.qa_chain.invoke({"context": context, "question": query})

        return response, source_docs_for_frontend