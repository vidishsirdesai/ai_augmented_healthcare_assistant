# AI Augmented Healthcare Assistant
## Idea
The idea is to build a LLM powered chat assistant for doctors that will help them query patient records, treatment guides, and drug interactions. And the responses needs to be really comprehensive and ofcourse very accurate because they are going to be used by doctors during patient consultations. Also, the doctors are going to ask follow-up questions.

The system should have an hybrid architecture combining both RAG and CAG. The details are as follows,
	- The system could first use RAG to retrieve the most relevant subset from the massive knowledge base, by pulling in specific sections of a particular patients's history and some research papers that are based on the doctor's query. Thereafter, instead of simply passing those retrieved chunks to the LLM, it could load all that retrieved content into a long context model that used CAG. Which then creates a temporary working memory for the specific patient case.
	- So in this hybrid approach, RAG's ability is used to efficiently search enormous knowledge bases, and CAG's ability is used to provide a full breadth of medical knowledge when needed for those follow-up questions without the system repeateadly querying the database.

The following technologies are to be used to build the app:
- Python 3.11.9
- Data Layer:
	- Create a sample datasets for each of the following,
		- mock_patient_records = [
			   {"id": "P001", "name": "Alice Smith", "age": 45, "diagnosis": "Type 2 Diabetes", "medications": "Metformin, Insulin", "history": "Diagnosed 5 years ago, occasional hyperglycemia, recent foot ulcer. Current lab results: HbA1c 8.2%, Glucose 250 mg/dL.", "notes": "Patient expresses concern about managing blood sugar levels during travel."},
			   {"id": "P002", "name": "Bob Johnson", "age": 62, "diagnosis": "Hypertension, Coronary Artery Disease (CAD)", "medications": "Lisinopril, Aspirin, Atorvastatin", "history": "History of Myocardial Infarction (MI) 3 years ago, controlled BP, occasional mild chest pain on exertion. Current lab results: Cholesterol 220 mg/dL, LDL 140 mg/dL.", "notes": "Patient is a smoker, advised to quit. Follow-up cardiology appointment scheduled."},
			   {"id": "P003", "name": "Carol White", "age": 30, "diagnosis": "Migraine with Aura", "medications": "Sumatriptan (as needed), Propranolol (prophylaxis)", "history": "Chronic migraines since adolescence, typically triggered by stress and certain foods. Experiences visual aura before onset. Recent increase in frequency.", "notes": "Discussed lifestyle modifications and potential for CGRP inhibitors."},
			   {"id": "P004", "name": "David Lee", "age": 55, "diagnosis": "Osteoarthritis (Knee)", "medications": "Naproxen (as needed), Glucosamine", "history": "Progressive knee pain, worse with activity. X-rays show moderate joint space narrowing. Patient is overweight.", "notes": "Recommended physical therapy and weight loss. Considering corticosteroid injection if conservative measures fail."},
			   {"id": "P005", "name": "Eva Green", "age": 28, "diagnosis": "Generalized Anxiety Disorder", "medications": "Escitalopram", "history": "Long-standing anxiety, panic attacks. Responds well to current medication but occasionally experiences breakthrough anxiety during high-stress periods.", "notes": "Referred for cognitive behavioral therapy (CBT). Discussed mindfulness techniques."},
			]
		- mock_treatment_guides = [
			   {"condition": "Type 2 Diabetes", "guide": "Initial management involves comprehensive lifestyle changes (dietary modifications, regular physical activity, weight management). If HbA1c remains elevated (typically >6.5-7.0%), Metformin is the recommended first-line pharmacological agent, unless contraindicated. Other oral agents or injectable therapies (e.g., GLP-1 receptor agonists, SGLM2 inhibitors) may be added or substituted based on individual patient factors, comorbidities, and glycemic targets. Insulin therapy is indicated for severe hyperglycemia, significant weight loss, or inadequate response to oral agents. Regular monitoring of blood glucose, HbA1c, renal function, and lipid profile is crucial. Comprehensive foot exams annually are essential for early detection of diabetic neuropathy and foot ulcers. Patient education on self-management is paramount."},
			   {"condition": "Hypertension", "guide": "Management of hypertension begins with lifestyle modifications including the DASH (Dietary Approaches to Stop Hypertension) eating plan, reduced sodium intake (<2300 mg/day, ideally <1500 mg/day), regular aerobic exercise (at least 150 minutes of moderate-intensity or 75 minutes of vigorous-intensity per week), moderation of alcohol consumption, and weight loss for overweight/obese individuals. First-line pharmacological agents include ACE inhibitors, Angiotensin Receptor Blockers (ARBs), Thiazide diuretics, and Calcium Channel Blockers (CCBs). The choice of agent depends on patient comorbidities, age, and individual response. Target blood pressure is generally <130/80 mmHg for most adults. Regular monitoring of blood pressure, electrolytes, and renal function is necessary."},
			   {"condition": "Migraine", "guide": "Acute migraine treatment involves simple analgesics (NSAIDs) for mild-to-moderate attacks. Triptans (e.g., Sumatriptan, Zolmitriptan) are specific serotonin receptor agonists effective for moderate-to-severe attacks. CGRP receptor antagonists (gepants) and serotonin 1F agonists (ditans) are newer acute options. Prophylactic treatment is considered for frequent or debilitating migraines (e.g., >4 headache days/month). Prophylactic agents include beta-blockers (Propranolol, Timolol), tricyclic antidepressants (Amitriptyline), anticonvulsants (Topiramate, Valproate), and CGRP monoclonal antibodies. Lifestyle management, stress reduction, and trigger avoidance are also important."},
			   {"condition": "Osteoarthritis", "guide": "Non-pharmacological management includes patient education, exercise (aerobic and strengthening), weight management, and physical therapy. Pharmacological options for pain relief include topical NSAIDs, oral NSAIDs, acetaminophen (paracetamol), and duloxetine. Intra-articular corticosteroid injections can provide temporary relief. Hyaluronic acid injections are also an option. Surgical interventions like arthroscopy or total joint replacement are considered for severe, refractory cases. Lifestyle adjustments to reduce joint stress are crucial."},
			   {"condition": "Generalized Anxiety Disorder", "guide": "Treatment typically involves psychotherapy (especially Cognitive Behavioral Therapy - CBT) and/or pharmacotherapy. First-line pharmacological agents include Selective Serotonin Reuptake Inhibitors (SSRIs) like Escitalopram and Sertraline, and Serotonin-Norepinephrine Reuptake Inhibitors (SNRIs) like Venlafaxine and Duloxetine. Benzodiazepines may be used for short-term relief of severe anxiety, but long-term use is generally discouraged due to dependence risk. Lifestyle interventions such as regular exercise, mindfulness, stress management techniques, and adequate sleep are also beneficial."},
			]
		- mock_drug_interactions = [
			   {"drug1": "Metformin", "drug2": "Iodinated Contrast Media", "interaction": "Risk of lactic acidosis. Metformin should be temporarily discontinued before and 48 hours after administration of iodinated contrast media in patients with risk factors for lactic acidosis (e.g., renal impairment)."},
			   {"drug1": "Lisinopril", "drug2": "Potassium Supplements", "interaction": "Increased risk of hyperkalemia. Concurrent use requires close monitoring of serum potassium levels, especially in patients with renal impairment or those also on potassium-sparing diuretics."},
			   {"drug1": "Aspirin", "drug2": "Warfarin", "interaction": "Increased risk of bleeding. Both are anticoagulants; concurrent use requires careful monitoring of INR and clinical signs of bleeding."},
			   {"drug1": "Sumatriptan", "drug2": "SSRIs/SNRIs", "interaction": "Risk of serotonin syndrome. Monitor for symptoms such as agitation, hallucinations, tachycardia, rapid blood pressure changes, hyperthermia, incoordination, nausea, vomiting, or diarrhea. Use with caution."},
			   {"drug1": "Naproxen", "drug2": "Lithium", "interaction": "NSAIDs like Naproxen can increase lithium levels, leading to toxicity. Monitor lithium levels closely."},
			   {"drug1": "Escitalopram", "drug2": "MAOIs", "interaction": "Contraindicated. Risk of serious, sometimes fatal, serotonin syndrome. A washout period is required when switching between these medications."},
			]
- AI/ ML Component:
	- HuggingFace Embeddings: `sentence-transformers/all-MiniLM-L6-v2` to generate embeddings of the text data.
	- ChromaDB Integration:
		- ChromaDB is to be used to store and retrieve vector embeddings.
		- A warning should be given if the ChromaDB is empty, indicating a need for data ingestion.
	- Connect to local Ollama instance using `mistral` model for text generation. Also include a connection test during initialization.
	- Use LangChain for RAG and CAG pipeline.
- Backend:
	- Technologies:
		- FastAPI
	- RESTful API Endpoints:
		- `POST /chat`: To ask natural language queries to the chatbot.
	- Pydantic Models for Data Validation:
		- ChatQuery: Validates incoming chat requests (ensuring query string).
		- ChatResponse: Defines the structure for chat responses.
	- Error Handling: Implements HTTPException for various errors, including RAG and CAG system initialization issues and unexpected errors.
	- CORS Middleware: Configured to allow cross-origin requests from any source (`*`).
	- Static File Serving: Serves the frontend HTML and other static assets from the /static directory.
	- Root Route: Serves the `index.html` file at the application's root URL (`/`).
- Frontend Interface:
	- Technologies:
		- HTML
		- CSS
		- JavaScript
	- UI:
		- The UI should have the chat assistant on the right side, and the results should be displayed on the left.