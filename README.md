# AI Augmented Healthcare Assistant
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
```

## Features
-

## Column Profiles
### `drug_interactions.json`
- `drug1`: Name of the first drug involved in the interaction.
- `drug2`: Name of the second drug involved in the interaction.
- `interaction`: A detailed description of the drug interaction, including risks and management advice.

### `patient_records.json`
- `id`: Unique identifier for the patient record.
- `name`: Patient's full name.
- `age`: Patient's age in years.
- `diagnosis`: The primary medical disgnosis of the patient.
- `medications`: A comma-separated list of medications the patient is currently on.
- `history`: A summary of the patient's medical history relevant to their diagnosis and current state.
- `notes`: Additional notes or specific concerns from the patient's visit.

### `treatment_guides.json`
- `condition`: The medical condition for which the guide provides treatment information.
- `guide`: A comprehensive guide outlining treatment strategies, including lifestyle, pharmacological, and other interventions.