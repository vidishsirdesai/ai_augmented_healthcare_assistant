# AI Augmented Healthcare Assistant
## Architecture
```mermaid
graph TD
    subgraph User Interface (Browser)
        A[index.html] -- Renders UI --> B(style.css)
        A -- Handles Interaction & API Calls --> C(script.js)
    end

    subgraph Backend (FastAPI Application)
        D[main.py] -- Initializes --> E(APIRouter)
        E -- Defines /chat endpoint --> F[endpoints.py]
        F -- Validates Input/Output --> G[models.py]
        G -- Uses LLM & RAG/CAG Pipeline --> H[rag_cag_pipeline.py]
        H -- Loads Configuration --> I[config.py]
        H -- Loads Raw Data --> J[data_loader.py]
    end

    subgraph External Services
        K[Ollama Server] -- Provides LLM --> H
    end

    subgraph Data Stores
        J -- Reads --> L[data/patient_records.json]
        J -- Reads --> M[data/treatment_guides.json]
        J -- Reads --> N[data/drug_interactions.json]
        H -- Ingests & Retrieves Embeddings --> O[ChromaDB (Vector Store)]
    end

    C -- "POST /chat Query" --> F
    F -- "Response + Sources" --> C

    H -- "LLM Inference Requests" --> K
    H -- "Embeddings Lookup & Storage" --> O
    O -- "Retrieved Context" --> H

    J -- "Processed Data" --> O

    style A fill:#DCE7F0,stroke:#3498db,stroke-width:2px,color:#2c3e50
    style B fill:#DCE7F0,stroke:#3498db,stroke-width:2px,color:#2c3e50
    style C fill:#DCE7F0,stroke:#3498db,stroke-width:2px,color:#2c3e50

    style D fill:#E8F8F5,stroke:#2ECC71,stroke-width:2px,color:#2c3e50
    style E fill:#E8F8F5,stroke:#2ECC71,stroke-width:2px,color:#2c3e50
    style F fill:#E8F8F5,stroke:#2ECC71,stroke-width:2px,color:#2c3e50
    style G fill:#E8F8F5,stroke:#2ECC71,stroke-width:2px,color:#2c3e50
    style H fill:#E8F8F5,stroke:#2ECC71,stroke-width:2px,color:#2c3e50
    style I fill:#E8F8F5,stroke:#2ECC71,stroke-width:2px,color:#2c3e50
    style J fill:#E8F8F5,stroke:#2ECC71,stroke-width:2px,color:#2c3e50

    style K fill:#F5EEF8,stroke:#9B59B6,stroke-width:2px,color:#2c3e50

    style L fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px,color:#2c3e50
    style M fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px,color:#2c3e50
    style N fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px,color:#2c3e50
    style O fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px,color:#2c3e50
```