# AI Augmented Healthcare Assistant
## Features
- 

## Architecture
```mermaid
graph TD
    subgraph UI
        A[index.html]
        B(style.css)
        C(script.js)
        A -- Renders UI --> B
        A -- Handles Interaction & API Calls --> C
    end

    subgraph Backend
        D[main.py]
        E(APIRouter)
        F[endpoints.py]
        G[models.py]
        H[rag_cag_pipeline.py]
        I[config.py]
        J[data_loader.py]

        D -- Initializes --> E
        E -- Defines /chat endpoint --> F
        F -- Validates Input/Output --> G
        G -- Uses LLM & RAG/CAG Pipeline --> H
        H -- Loads Configuration --> I
        H -- Loads Raw Data --> J
    end

    subgraph External Services
        K[Ollama Server]
        K -- Provides LLM --> H
    end

    subgraph Data Stores
        L[data/patient_records.json]
        M[data/treatment_guides.json]
        N[data/drug_interactions.json]
        O[Vector Store]

        J -- Reads --> L
        J -- Reads --> M
        J -- Reads --> N
        H -- Ingests & Retrieves Embeddings --> O
    end

    C -- "POST /chat Query" --> F
    F -- "Response + Sources" --> C

    H -- "LLM Inference Requests" --> K
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