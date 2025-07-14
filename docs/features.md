# Features
## Core Features
- Retrieval-Augmented Generation (RAG) Pipeline: The application uses a RAG pipeline to generate informed responses by first retrieving relevant information from its knowledge base and then using an LLM to formulate an answer based on that context.
- Cache-Augmented Generation (CAG) Pipeline: Implemented using `functools.lru_cache`, this feature caches recent query results to enable faster responses for identical subsequent queries, bypassing redundant retrieval and LLM interface. The cache is automatically cleared when the application is re-initialized or when new data is ingested, ensuring data freshness.
- Ollam Integration: Utilizes Ollama as the backend for serving large language models (LLMs) allowing for flexible local or self-hosted LLM deployment.
- HuggingFace Embeddings: Employs `HuggingFaceEmbeddings` to convert text data into numerical vectors, enabling efficient semantic search and retrieval.
- ChromaDB Vector Store: Uses ChromaDB as a persistent vector database to store and efficiently search through embedded medical documents.

## Data Management & Knowledge Base
- Multi-Source Data Ingestion: Can ingest data from different healthcare domains, including:
	- Drug Interactions: Specific details about interactions between different medications, including risks and management.
	- Patient Records: Detailed patient information like id, name, age, diagnosis, medications, history, and notes
	- Treatment Guides: Comprehensive information on managing various medical conditions.
- Document Chunking: Automatically splits large documents into smaller, manageable chunks using `RecursiveCharacterTextSplitter` to optimize retrieval and context feeding to the LLM.
- Persistent Knowledge Base: ChromaDB ensures that ingested data and its embeddings are persistently stored, so the knowledge base does not need to be rebuilt with every application restart.

## User Interface & Interaction
- Interactive Chat Interface: Provides a real-time chat experience where users can input queries and receive AI-generated responses.
- Source Document Display: Displays the specific source documents (patient records, treatment guides, and drug interactions) that the AI used to formulate its answer, enhancing transparency and trustworthiness.
- Dynamic UI Updates: JavaScript handles sending queries to the backend and dynamically updating the chatbox and source document display with responses and retrieved information.
- Loading & Error Status: Provides visual feedback to the user, indicating when the AI is "thinking", or if an error occurred during the request.
- Input Validation: The frontend ensures that queries are not empty before sending them.

## Backend & API
- FastAPI Backend: A modern, high-performance web framework for building the API endpoints.
- Asynchronous Operations: The backend utilizes `async`/ `await` for non-blocking I/O operations, particularly for API calls and potentially for Ollama interactions, improving responsiveness.
- Structured API Endpoints: Defines clear API endpoints (e.g., `/chat`) for communication between the frontend and the RAG-CAG pipeline.
- Pydantic Models: Uses Pydantic for data validation and serialization of API requests and responses, ensuring data consistency and type safety.
- Centralized Configuration: Employs a `config.py` file to manage environment-specific settings, making the application configurable and portable.
- Ollama Connection Testing: The pipeline includes a mechanism to test connectivity to the Ollama server and verify the availability of the specified LLM model at startup.
