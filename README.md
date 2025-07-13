# AI Augmented Healthcare Assistant
## Features

This is the first part of the prompt:

The project file structure is as follows,

```
ai_augmented_healthcare_assistant/
├── data/
│   └── drug_interactions.json
│   ├── patient_records.json
│   ├── treatment_guides.json
├── data/
│   ├── file_structure.md
├── src/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── rag_cag_pipeline.py
│   │   └── data_loader.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
├── README.md
└── requirements.txt
```

The contents of ai_augmented_healthcare_assistant/data/drug_interactions.json are,

[
    {"drug1": "Metformin", "drug2": "Iodinated Contrast Media", "interaction": "Risk of lactic acidosis. Metformin should be temporarily discontinued before and 48 hours after administration of iodinated contrast media in patients with risk factors for lactic acidosis (e.g., renal impairment)."},
    {"drug1": "Lisinopril", "drug2": "Potassium Supplements", "interaction": "Increased risk of hyperkalemia. Concurrent use requires close monitoring of serum potassium levels, especially in patients with renal impairment or those also on potassium-sparing diuretics."},
    {"drug1": "Aspirin", "drug2": "Warfarin", "interaction": "Increased risk of bleeding. Both are anticoagulants; concurrent use requires careful monitoring of INR and clinical signs of bleeding."},
    {"drug1": "Sumatriptan", "drug2": "SSRIs/SNRIs", "interaction": "Risk of serotonin syndrome. Monitor for symptoms such as agitation, hallucinations, tachycardia, rapid blood pressure changes, hyperthermia, incoordination, nausea, vomiting, or diarrhea. Use with caution."},
    {"drug1": "Naproxen", "drug2": "Lithium", "interaction": "NSAIDs like Naproxen can increase lithium levels, leading to toxicity. Monitor lithium levels closely."},
    {"drug1": "Escitalopram", "drug2": "MAOIs", "interaction": "Contraindicated. Risk of serious, sometimes fatal, serotonin syndrome. A washout period is required when switching between these medications."},
    {"drug1": "Digoxin", "drug2": "Amiodarone", "interaction": "Increased digoxin levels, leading to toxicity. Reduce digoxin dose by 50% when initiating amiodarone and monitor digoxin levels closely."},
    {"drug1": "Warfarin", "drug2": "Amiodarone", "interaction": "Significantly increased anticoagulant effect of warfarin, increasing bleeding risk. Reduce warfarin dose by 30-50% and monitor INR frequently when initiating amiodarone."},
    {"drug1": "Simvastatin", "drug2": "Clarithromycin", "interaction": "Increased risk of statin-induced myopathy/rhabdomyolysis due to inhibition of CYP3A4. Avoid concurrent use or use alternative statin not metabolized by CYP3A4."},
    {"drug1": "Phenytoin", "drug2": "Oral Contraceptives", "interaction": "Decreased efficacy of oral contraceptives due to enzyme induction. Advise use of alternative non-hormonal contraception."},
    {"drug1": "Spironolactone", "drug2": "ACE Inhibitors", "interaction": "Increased risk of severe hyperkalemia. Close monitoring of potassium levels is essential, especially in patients with impaired renal function."},
    {"drug1": "Sildenafil", "drug2": "Nitrates", "interaction": "Potentiation of hypotensive effects, leading to severe and potentially fatal hypotension. Concomitant use is contraindicated."},
    {"drug1": "Levothyroxine", "drug2": "Calcium Carbonate", "interaction": "Reduced absorption of levothyroxine. Separate administration by at least 4 hours."},
    {"drug1": "Methotrexate", "drug2": "NSAIDs", "interaction": "Increased methotrexate levels, leading to toxicity (e.g., bone marrow suppression). Use with extreme caution and monitor for signs of toxicity."},
    {"drug1": "Insulin", "drug2": "Beta-blockers", "interaction": "Masking of hypoglycemia symptoms (e.g., tremors, palpitations) and potential for prolonged hypoglycemia. Patients should be warned about this interaction and taught to recognize other signs of hypoglycemia."},
    {"drug1": "Citalopram", "drug2": "QT Prolonging Drugs", "interaction": "Increased risk of QT interval prolongation and Torsade de Pointes. Avoid co-administration with other drugs known to prolong the QT interval."},
    {"drug1": "Rifampin", "drug2": "Warfarin", "interaction": "Decreased anticoagulant effect of warfarin due to enzyme induction. Requires significant increase in warfarin dose and frequent INR monitoring."},
    {"drug1": "Fluoxetine", "drug2": "Triptans", "interaction": "Increased risk of serotonin syndrome. Monitor patients for symptoms if co-administered."}
]

The contents of ai_augmented_healthcare_assistant/data/patient_records.json are,

[
    {"id": "P001", "name": "Alice Smith", "age": 45, "diagnosis": "Type 2 Diabetes", "medications": "Metformin, Insulin", "history": "Diagnosed 5 years ago, occasional hyperglycemia, recent foot ulcer. Current lab results: HbA1c 8.2%, Glucose 250 mg/dL.", "notes": "Patient expresses concern about managing blood sugar levels during travel."},
    {"id": "P002", "name": "Bob Johnson", "age": 62, "diagnosis": "Hypertension, Coronary Artery Disease (CAD)", "medications": "Lisinopril, Aspirin, Atorvastatin", "history": "History of Myocardial Infarction (MI) 3 years ago, controlled BP, occasional mild chest pain on exertion. Current lab results: Cholesterol 220 mg/dL, LDL 140 mg/dL.", "notes": "Patient is a smoker, advised to quit. Follow-up cardiology appointment scheduled."},
    {"id": "P003", "name": "Carol White", "age": 30, "diagnosis": "Migraine with Aura", "medications": "Sumatriptan (as needed), Propranolol (prophylaxis)", "history": "Chronic migraines since adolescence, typically triggered by stress and certain foods. Experiences visual aura before onset. Recent increase in frequency.", "notes": "Discussed lifestyle modifications and potential for CGRP inhibitors."},
    {"id": "P004", "name": "David Lee", "age": 55, "diagnosis": "Osteoarthritis (Knee)", "medications": "Naproxen (as needed), Glucosamine", "history": "Progressive knee pain, worse with activity. X-rays show moderate joint space narrowing. Patient is overweight.", "notes": "Recommended physical therapy and weight loss. Considering corticosteroid injection if conservative measures fail."},
    {"id": "P005", "name": "Eva Green", "age": 28, "diagnosis": "Generalized Anxiety Disorder", "medications": "Escitalopram", "history": "Long-standing anxiety, panic attacks. Responds well to current medication but occasionally experiences breakthrough anxiety during high-stress periods.", "notes": "Referred for cognitive behavioral therapy (CBT). Discussed mindfulness techniques."},
    {"id": "P006", "name": "Frank Miller", "age": 70, "diagnosis": "Chronic Kidney Disease (Stage 3)", "medications": "Furosemide, Calcium Acetate", "history": "Gradual decline in renal function over 10 years. Managed with diet and medication. Occasional edema. Current lab results: eGFR 40 mL/min/1.73m², Creatinine 1.8 mg/dL.", "notes": "Educated on low-sodium, low-potassium diet. Follow-up with nephrologist in 3 months."},
    {"id": "P007", "name": "Grace Hall", "age": 50, "diagnosis": "Rheumatoid Arthritis", "medications": "Methotrexate, Folic Acid", "history": "Diagnosed 2 years ago, complains of joint stiffness and pain in hands and feet. Currently experiencing a flare-up. ESR 45 mm/hr, CRP 15 mg/L.", "notes": "Considered increasing Methotrexate dose, but opted for a short course of prednisone for flare. Advised regular exercise."},
    {"id": "P008", "name": "Henry Clark", "age": 35, "diagnosis": "Crohn's Disease", "medications": "Adalimumab", "history": "Diagnosed in early 20s. Managed with biologics, occasional abdominal pain and diarrhea. Recent colonoscopy showed mild inflammation.", "notes": "Discussed diet triggers. Scheduled for routine blood work to monitor drug levels and inflammation markers."},
    {"id": "P009", "name": "Ivy Baker", "age": 22, "diagnosis": "Anorexia Nervosa", "medications": "None", "history": "Patient recently hospitalized for severe malnutrition. Engaged in refeeding program. Struggles with body image. BMI 16.2 kg/m².", "notes": "Multidisciplinary team approach initiated (nutritionist, psychiatrist). Weekly weight checks."},
    {"id": "P010", "name": "Jack Adams", "age": 68, "diagnosis": "Benign Prostatic Hyperplasia (BPH)", "medications": "Tamsulosin", "history": "Progressive difficulty with urination, nocturia. PSA levels stable. Digital rectal exam (DRE) consistent with BPH.", "notes": "Discussed lifestyle changes (fluid intake). Advised to report any acute urinary retention."},
    {"id": "P011", "name": "Karen Young", "age": 40, "diagnosis": "Hypothyroidism", "medications": "Levothyroxine", "history": "Diagnosed 3 years ago. Reports fatigue and weight gain if medication is not consistent. Current TSH 4.8 mIU/L (slightly elevated).", "notes": "Adjusted Levothyroxine dose. Advised taking medication on an empty stomach consistently."},
    {"id": "P012", "name": "Liam Scott", "age": 14, "diagnosis": "Asthma", "medications": "Albuterol (as needed), Fluticasone (daily)", "history": "Childhood asthma, well-controlled with daily inhaled corticosteroid. Occasional rescue inhaler use during exercise or colds. Peak flow readings within normal limits.", "notes": "Reviewed inhaler technique. Discussed importance of adherence to daily medication."},
    {"id": "P013", "name": "Mia King", "age": 29, "diagnosis": "Polycystic Ovary Syndrome (PCOS)", "medications": "Metformin, Oral Contraceptives", "history": "Irregular periods, hirsutism, insulin resistance. Trying to conceive. Lab results: elevated androgens.", "notes": "Discussed weight management and fertility options. Referred to endocrinologist."},
    {"id": "P014", "name": "Noah Turner", "age": 58, "diagnosis": "Gout", "medications": "Allopurinol (daily), Colchicine (as needed)", "history": "Recurrent acute gout attacks, primarily in the big toe. Elevated uric acid levels. Recent flare-up.", "notes": "Advised on dietary modifications (avoid high-purine foods). Emphasized medication adherence."},
    {"id": "P015", "name": "Olivia Hill", "age": 75, "diagnosis": "Osteoporosis", "medications": "Alendronate", "history": "Diagnosed after a hip fracture 2 years ago. DEXA scan shows T-score -2.8. No recent falls.", "notes": "Reviewed fall prevention strategies. Emphasized calcium and Vitamin D intake. Scheduled next DEXA scan."}
]


The contents of ai_augmented_healthcare_assistant/data/treatment_guides.json are,

[
    {"condition": "Type 2 Diabetes", "guide": "Initial management involves comprehensive lifestyle changes (dietary modifications, regular physical activity, weight management). If HbA1c remains elevated (typically >6.5-7.0%), Metformin is the recommended first-line pharmacological agent, unless contraindicated. Other oral agents or injectable therapies (e.g., GLP-1 receptor agonists, SGLM2 inhibitors) may be added or substituted based on individual patient factors, comorbidities, and glycemic targets. Insulin therapy is indicated for severe hyperglycemia, significant weight loss, or inadequate response to oral agents. Regular monitoring of blood glucose, HbA1c, renal function, and lipid profile is crucial. Comprehensive foot exams annually are essential for early detection of diabetic neuropathy and foot ulcers. Patient education on self-management is paramount."},
    {"condition": "Hypertension", "guide": "Management of hypertension begins with lifestyle modifications including the DASH (Dietary Approaches to Stop Hypertension) eating plan, reduced sodium intake (<2300 mg/day, ideally <1500 mg/day), regular aerobic exercise (at least 150 minutes of moderate-intensity or 75 minutes of vigorous-intensity per week), moderation of alcohol consumption, and weight loss for overweight/obese individuals. First-line pharmacological agents include ACE inhibitors, Angiotensin Receptor Blockers (ARBs), Thiazide diuretics, and Calcium Channel Blockers (CCBs). The choice of agent depends on patient comorbidities, age, and individual response. Target blood pressure is generally <130/80 mmHg for most adults. Regular monitoring of blood pressure, electrolytes, and renal function is necessary."},
    {"condition": "Migraine", "guide": "Acute migraine treatment involves simple analgesics (NSAIDs) for mild-to-moderate attacks. Triptans (e.g., Sumatriptan, Zolmitriptan) are specific serotonin receptor agonists effective for moderate-to-severe attacks. CGRP receptor antagonists (gepants) and serotonin 1F agonists (ditans) are newer acute options. Prophylactic treatment is considered for frequent or debilitating migraines (e.g., >4 headache days/month). Prophylactic agents include beta-blockers (Propranolol, Timolol), tricyclic antidepressants (Amitriptyline), anticonvulsants (Topiramate, Valproate), and CGRP monoclonal antibodies. Lifestyle management, stress reduction, and trigger avoidance are also important."},
    {"condition": "Osteoarthritis", "guide": "Non-pharmacological management includes patient education, exercise (aerobic and strengthening), weight management, and physical therapy. Pharmacological options for pain relief include topical NSAIDs, oral NSAIDs, acetaminophen (paracetamol), and duloxetine. Intra-articular corticosteroid injections can provide temporary relief. Hyaluronic acid injections are also an option. Surgical interventions like arthroscopy or total joint replacement are considered for severe, refractory cases. Lifestyle adjustments to reduce joint stress are crucial."},
    {"condition": "Generalized Anxiety Disorder", "guide": "Treatment typically involves psychotherapy (especially Cognitive Behavioral Therapy - CBT) and/or pharmacotherapy. First-line pharmacological agents include Selective Serotonin Reuptake Inhibitors (SSRIs) like Escitalopram and Sertraline, and Serotonin-Norepinephrine Reuptake Inhibitors (SNRIs) like Venlafaxine and Duloxetine. Benzodiazepines may be used for short-term relief of severe anxiety, but long-term use is generally discouraged due to dependence risk. Lifestyle interventions such as regular exercise, mindfulness, stress management techniques, and adequate sleep are also beneficial."},
    {"condition": "Chronic Kidney Disease (CKD)", "guide": "Management focuses on slowing progression and managing complications. Key strategies include blood pressure control (target <130/80 mmHg, often with ACE inhibitors/ARBs), glycemic control in diabetics (HbA1c targets individualized), dietary protein restriction (0.8 g/kg/day for non-dialysis CKD), sodium restriction, and treatment of dyslipidemia. Anemia, bone and mineral disorders, and acidosis should also be addressed. Avoidance of nephrotoxic drugs (e.g., NSAIDs, certain antibiotics) is critical. Regular monitoring of eGFR, creatinine, electrolytes, and albuminuria is essential. Referral to a nephrologist is indicated for progressive CKD or advanced stages."},
    {"condition": "Rheumatoid Arthritis (RA)", "guide": "Early diagnosis and aggressive treatment are crucial to prevent joint damage. Disease-Modifying Antirheumatic Drugs (DMARDs) are the cornerstone of therapy, with Methotrexate often being the first-line conventional synthetic DMARD. Biologic DMARDs and targeted synthetic DMARDs (JAK inhibitors) are used for patients with inadequate response to conventional DMARDs. Glucocorticoids may be used for short-term symptom control during flares or initiation of DMARDs. NSAIDs provide symptomatic relief but do not alter disease progression. Physical and occupational therapy are important for maintaining joint function and reducing pain. Regular monitoring of disease activity and adverse effects of medication is necessary."},
    {"condition": "Crohn's Disease", "guide": "Treatment aims to induce and maintain remission, manage symptoms, and prevent complications. 5-aminosalicylates (5-ASAs) may be used for mild disease. Corticosteroids are used for inducing remission in moderate-to-severe flares but not for long-term maintenance. Immunomodulators (e.g., Azathioprine, Methotrexate) and biologics (e.g., anti-TNF agents, anti-integrins) are used for moderate-to-severe disease and for maintaining remission. Diet modification, nutritional support, and smoking cessation are important adjuncts. Surgical intervention may be necessary for complications like strictures or fistulas."},
    {"condition": "Anorexia Nervosa", "guide": "Treatment requires a multidisciplinary approach involving medical, psychological, and nutritional support. The primary goal is weight restoration and normalization of eating behaviors. Family-Based Treatment (FBT) is highly effective for adolescents. Cognitive Behavioral Therapy (CBT) and other psychotherapies are used for adults. Nutritional rehabilitation includes structured meal plans and refeeding protocols to prevent refeeding syndrome. Close medical monitoring for electrolyte imbalances, cardiac complications, and other medical instabilities is crucial. Addressing underlying psychological issues and body image distortions is central to long-term recovery."},
    {"condition": "Benign Prostatic Hyperplasia (BPH)", "guide": "Management depends on symptom severity. Lifestyle modifications include limiting fluid intake before bed, avoiding caffeine and alcohol, and timed voiding. Pharmacological options include alpha-1 blockers (e.g., Tamsulosin, Alfuzosin) to relax prostate muscles, and 5-alpha-reductase inhibitors (e.g., Finasteride, Dutasteride) to reduce prostate size. Combination therapy may be used. Surgical interventions (e.g., TURP - Transurethral Resection of the Prostate) are considered for severe symptoms, complications, or failed medical therapy."},
    {"condition": "Hypothyroidism", "guide": "The standard treatment is lifelong thyroid hormone replacement therapy with synthetic Levothyroxine. The dose is individualized based on patient age, weight, cardiovascular status, and most importantly, serum TSH levels. TSH levels are typically monitored every 6-8 weeks initially after dose adjustments and then annually once stable. Patients should be advised to take levothyroxine consistently on an empty stomach, usually in the morning, and separate from other medications or supplements (especially calcium, iron, and antacids) by at least 4 hours. Symptoms should improve gradually over weeks to months once optimal thyroid levels are achieved."},
    {"condition": "Asthma", "guide": "Management involves a stepped approach based on asthma severity and control. All patients should have a short-acting beta-agonist (SABA, e.g., Albuterol) for quick relief of symptoms. Long-term control medications include inhaled corticosteroids (ICS) as the preferred first-line therapy for persistent asthma. Long-acting beta-agonists (LABAs) are often added to ICS for better control. Leukotriene modifiers and biologic therapies may be used for specific phenotypes or severe persistent asthma. Patient education on trigger avoidance, inhaler technique, and personalized action plans is vital. Regular follow-up and assessment of asthma control are essential."},
    {"condition": "Polycystic Ovary Syndrome (PCOS)", "guide": "Management is individualized based on symptoms and patient goals (e.g., fertility, menstrual regularity, hirsutism, metabolic health). Lifestyle modifications (diet, exercise, weight loss) are foundational. Oral contraceptives are commonly used to regulate menstrual cycles and manage hirsutism. Metformin may be used for insulin resistance, especially if impaired glucose tolerance is present. For infertility, ovulation induction (e.g., Clomiphene, Letrozole) or assisted reproductive technologies may be considered. Hirsutism can be managed with anti-androgens or cosmetic treatments. Regular screening for diabetes, dyslipidemia, and cardiovascular risk factors is important."},
    {"condition": "Gout", "guide": "Acute gout attacks are managed with NSAIDs, colchicine, or corticosteroids. Long-term management focuses on urate-lowering therapy (ULT) to prevent future attacks. Allopurinol is the most commonly used first-line ULT, followed by Febuxostat or Uricase inhibitors (e.g., Pegloticase) for refractory cases. ULT should be initiated or continued during an acute attack after anti-inflammatory treatment has begun. Lifestyle modifications including dietary changes (limiting high-purine foods, sugary drinks, alcohol) and weight management are important adjunctive therapies. Regular monitoring of serum uric acid levels is necessary to achieve and maintain target levels."},
    {"condition": "Osteoporosis", "guide": "Management aims to prevent fractures. Non-pharmacological measures include adequate calcium (1000-1200 mg/day) and Vitamin D (600-800 IU/day for adults <70, 800-1000 IU/day for adults >70) intake, weight-bearing exercise, and fall prevention strategies. Pharmacological treatments include bisphosphonates (e.g., Alendronate, Risedronate) as first-line for most patients. Other options include denosumab, teriparatide, abaloparatide, and romosozumab, chosen based on fracture risk and patient characteristics. Regular bone mineral density (BMD) monitoring via DEXA scans is recommended to assess treatment effectiveness and guide therapy duration."}
]

The contents of ai_augmented_healthcare_assistant/src/api/endpoints.py are,

# src/api/endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from src.api.models import ChatQuery, ChatResponse
from src.core.rag_cag_pipeline import RAGCAGPipeline

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    chat_query: ChatQuery,
    # Corrected access: import 'src.main' then get the attribute from the returned module
    rag_cag_pipeline_instance: RAGCAGPipeline = Depends(lambda: __import__("src.main").main.get_rag_cag_pipeline_dependency())
):
    """
    Receives a natural language query from the doctor and returns a comprehensive response.
    """
    try:
        response, sources = await rag_cag_pipeline_instance.process_query(chat_query.query)
        return ChatResponse(response=response, source_documents=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

The contents of ai_augmented_healthcare_assistant/src/api/models.py are,

# src/api/models.py
from pydantic import BaseModel, Field

class ChatQuery(BaseModel):
    query: str = Field(..., min_length=1, example="What is the treatment for Type 2 Diabetes for patient Alice Smith?")

class ChatResponse(BaseModel):
    response: str = Field(..., example="The recommended treatment for Type 2 Diabetes involves lifestyle changes and Metformin.")
    source_documents: list[dict] = Field(default_factory=list, example=[{"content": "...", "metadata": {"source": "patient_records", "id": "P001"}}])

The contents of ai_augmented_healthcare_assistant/src/core/models.py are,

# src/core/config.py
import os

class Settings:
    # Ollama configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")

    # ChromaDB configuration
    CHROMADB_PATH: str = os.getenv("CHROMADB_PATH", "./chroma_db")

    # Embedding model
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Data paths
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    PATIENT_RECORDS_PATH: str = os.path.join(DATA_DIR, "patient_records.json")
    TREATMENT_GUIDES_PATH: str = os.path.join(DATA_DIR, "treatment_guides.json")
    DRUG_INTERACTIONS_PATH: str = os.path.join(DATA_DIR, "drug_interactions.json")

settings = Settings()

The contents of ai_augmented_healthcare_assistant/src/core/data_loader.py are,

# src/core/data_loader.py
import json
import os

class DataLoader:
    def load_data(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

This is the second part of the prompt:

The contents of ai_augmented_healthcare_assistant/src/core/rag_cag_pipeline.py are,

# src/core/rag_cag_pipeline.py
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA # May be removed if not directly used later
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import BaseMessage
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

        self.llm = OllamaLLM(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL, temperature=0.1)


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
        self._ensure_embeddings_and_vectorstore()

        documents = []
        for item in data:
            content = ""
            metadata = {}

            if data_type == "patient_records":
                content = (
                    f"Patient ID: {str(item.get('id', 'N/A'))}\n"
                    f"Name: {str(item.get('name', 'N/A'))}\n"
                    f"Age: {str(item.get('age', 'N/A'))}\n"
                    f"Diagnosis: {str(item.get('diagnosis', 'N/A'))}\n"
                    f"Medications: {str(item.get('medications', 'N/A'))}\n"
                    f"History: {str(item.get('history', 'N/A'))}\n"
                    f"Notes: {str(item.get('notes', 'N/A'))}"
                )
                metadata = {"source": "patient_records", "id": str(item.get('id', 'N/A'))}
            elif data_type == "treatment_guides":
                content = (
                    f"Condition: {str(item.get('condition', 'N/A'))}\n"
                    f"Guide: {str(item.get('guide', 'N/A'))}"
                )
                metadata = {"source": "treatment_guides", "condition": str(item.get('condition', 'N/A'))}
            elif data_type == "drug_interactions":
                content = (
                    f"Drug 1: {str(item.get('drug1', 'N/A'))}\n"
                    f"Drug 2: {str(item.get('drug2', 'N/A'))}\n"
                    f"Interaction: {str(item.get('interaction', 'N/A'))}"
                )
                metadata = {
                    "source": "drug_interactions",
                    "drug1": str(item.get('drug1', 'N/A')),
                    "drug2": str(item.get('drug2', 'N/A'))
                }
            else:
                continue

            if not isinstance(content, str):
                print(f"Warning: Final Document content for {data_type} is not a string after initial formatting. Converting. Content: {content}")
                content = str(content)

            documents.append(Document(page_content=content, metadata=metadata))

        if documents:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_documents = text_splitter.split_documents(documents)

            print(f"Adding {len(split_documents)} documents from {data_type} to ChromaDB...")
            self.vectorstore.add_documents(split_documents)
            print(f"Successfully ingested {len(split_documents)} documents for {data_type}.")
        else:
            print(f"No documents to ingest for {data_type}.")

    def _setup_qa_chain(self):
        """Sets up the LangChain QA chain for RAG and prepares for CAG."""
        self._ensure_embeddings_and_vectorstore()
        if not self.llm:
            raise RuntimeError("LLM not initialized when trying to setup QA chain.")
           
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

        # FIX: Explicitly define the chain to accept 'question' and retrieve context
        # This structure ensures that the prompt receives a dict with 'context' and 'question' strings.
        self.qa_chain = (
            # Step 1: Accept the raw 'question' string input.
            # Step 2: Use RunnablePassthrough.assign to create the 'context' and pass 'question' through.
            {
                "context": self.retriever | (lambda docs: "\n\n".join([str(doc.page_content) for doc in docs])),
                "question": RunnablePassthrough()
            }
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
        if not self.qa_chain:
            try:
                self._setup_qa_chain()
            except RuntimeError as e:
                return f"The knowledge base is not yet fully ready for queries: {e}", []

        # It's good practice to ensure self.retriever is ready before invoking for source docs
        if not self.retriever:
            try:
                self._setup_qa_chain() # Try to set up if not already
            except RuntimeError as e:
                return f"Retrieval component not ready: {e}", []

        # Perform retrieval *separately* if you want to explicitly get source_docs_for_frontend
        retrieved_docs = self.retriever.invoke(query)
        
        source_docs_for_frontend = [
            {"content": str(doc.page_content), "metadata": doc.metadata} 
            for doc in retrieved_docs
        ]

        # The qa_chain now expects a dictionary with both 'question' and 'context' (or just 'question' for retrieval).
        # We pass only the 'question' key, and the chain itself handles the retrieval for 'context'.
        response = self.qa_chain.invoke(query) # Pass the raw query string as input

        return response, source_docs_for_frontend

The contents of ai_augmented_healthcare_assistant/src/static/index.html are,

<!-- src/static/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Healthcare Assistant</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <div class="left-panel">
            <h2>Source Documents</h2>
            <div id="source-documents" class="source-documents-container">
                <p>Relevant information from patient records, treatment guides, and drug interactions will appear here.</p>
            </div>
        </div>
        <div class="right-panel">
            <h1>AI Healthcare Assistant Chat</h1>
            <div id="chat-box" class="chat-box">
                <div class="message bot-message">
                    Hello! I'm your AI Healthcare Assistant. How can I help you today?
                </div>
            </div>
            <form id="chat-form" class="chat-input-form">
                <input type="text" id="user-input" placeholder="Ask a medical question..." required>
                <button type="submit">Send</button>
            </form>
            <div id="status-message" class="status-message"></div>
        </div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>

The contents of ai_augmented_healthcare_assistant/src/static/script.js are,

// src/static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const statusMessage = document.getElementById('status-message');
    const sourceDocumentsDiv = document.getElementById('source-documents');

    const API_BASE_URL = window.location.origin; // Dynamically get base URL

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        addMessageToChatBox(query, 'user-message');
        userInput.value = '';
        statusMessage.textContent = 'Thinking...';
        sourceDocumentsDiv.innerHTML = '<p>Retrieving and generating...</p>'; // Clear and show loading

        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Something went wrong on the server.');
            }

            const data = await response.json();
            addMessageToChatBox(data.response, 'bot-message');
            displaySourceDocuments(data.source_documents);
            statusMessage.textContent = '';

        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = `Error: ${error.message}`;
            addMessageToChatBox('Sorry, I am unable to process your request at the moment. Please try again later.', 'bot-message');
            sourceDocumentsDiv.innerHTML = '<p>Failed to load source documents.</p>';
        } finally {
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        }
    });

    function addMessageToChatBox(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function displaySourceDocuments(documents) {
        sourceDocumentsDiv.innerHTML = ''; // Clear previous documents
        if (documents && documents.length > 0) {
            documents.forEach(doc => {
                const docDiv = document.createElement('div');
                docDiv.classList.add('source-document');
                let content = doc.content.length > 300 ? doc.content.substring(0, 300) + '...' : doc.content;
                let metadataHtml = '';
                if (doc.metadata) {
                    metadataHtml += '<strong>Source:</strong> ' + (doc.metadata.source || 'N/A');
                    if (doc.metadata.id) metadataHtml += `, <strong>ID:</strong> ${doc.metadata.id}`;
                    if (doc.metadata.condition) metadataHtml += `, <strong>Condition:</strong> ${doc.metadata.condition}`;
                    if (doc.metadata.drug1) metadataHtml += `, <strong>Drug1:</strong> ${doc.metadata.drug1}`;
                    if (doc.metadata.drug2) metadataHtml += `, <strong>Drug2:</strong> ${doc.metadata.drug2}`;
                }
                docDiv.innerHTML = `<p>${content}</p><p class="metadata">${metadataHtml}</p>`;
                sourceDocumentsDiv.appendChild(docDiv);
            });
        } else {
            sourceDocumentsDiv.innerHTML = '<p>No specific source documents retrieved for this query, or the information was generated from broad knowledge.</p>';
        }
    }
});

The contents of ai_augmented_healthcare_assistant/src/static/style.js are,

/* src/static/style.css */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f7f6;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.container {
    display: flex;
    width: 90%;
    max-width: 1400px;
    height: 80vh;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.left-panel, .right-panel {
    padding: 20px;
    box-sizing: border-box;
}

.left-panel {
    flex: 1;
    border-right: 1px solid #eee;
    background-color: #f9f9f9;
    overflow-y: auto;
}

.left-panel h2 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

.source-documents-container {
    font-size: 0.9em;
    color: #555;
}

.source-document {
    background-color: #e8f0f8;
    border-left: 4px solid #3498db;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 4px;
}

.source-document strong {
    color: #2c3e50;
}

.right-panel {
    flex: 2;
    display: flex;
    flex-direction: column;
}

.right-panel h1 {
    color: #2c3e50;
    text-align: center;
    margin-bottom: 20px;
}

.chat-box {
    flex-grow: 1;
    overflow-y: auto;
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    margin-bottom: 15px;
    background-color: #fafafa;
}

.message {
    max-width: 80%;
    padding: 10px 15px;
    border-radius: 20px;
    margin-bottom: 10px;
    line-height: 1.4;
}

.user-message {
    background-color: #dcf8c6;
    align-self: flex-end;
    margin-left: auto;
    text-align: right;
}

.bot-message {
    background-color: #e5e5ea;
    align-self: flex-start;
    text-align: left;
}

.chat-input-form {
    display: flex;
    gap: 10px;
}

.chat-input-form input[type="text"] {
    flex-grow: 1;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 25px;
    font-size: 1em;
}

.chat-input-form button {
    padding: 12px 25px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.3s ease;
}

.chat-input-form button:hover {
    background-color: #2980b9;
}

.status-message {
    margin-top: 10px;
    font-size: 0.9em;
    color: #e74c3c;
    text-align: center;
}

Generate a mermaid flowchart diagram of the architecture.

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