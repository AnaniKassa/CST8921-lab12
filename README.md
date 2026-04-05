# About me 
### Full name: Anani Thierry Kassa
### Student ID: 041140713

## Lab Modules
### Module 1 — Provision Azure Resources
Tasks
Create the following resources in Azure Portal:
1.	Resource Group: rg-ai-search-lab
![alt text](./1-1.PNG)
2.	Azure AI Search service: srch-rag-lab
![alt text](./1-2.PNG)
3.	Pricing tier: choose a lab-appropriate tier
4.	Azure OpenAI / Azure AI Foundry-backed OpenAI resource: aoai-rag-lab
![alt text](./1-3.PNG)
5.	Storage Account : stsearchlabfiles 
![alt text](./1-4.PNG)
6.	Optional: Azure AI Foundry project for model management
![alt text](./1-5.PNG)

### Module 2 — Deploy Embedding and LLM Models
1.	Open Azure OpenAI / Foundry
2.	Create model deployment for embeddings
3.	Create model deployment for chat
4.	Save:
•	Endpoint
•	API key
•	deployment names
- Students should record:
•	AZURE_OPENAI_ENDPOINT
![alt text](./2-1.PNG)
•	AZURE_OPENAI_API_KEY
•	EMBEDDING_MODEL_DEPLOYMENT
•	CHAT_MODEL_DEPLOYMENT
![alt text](./2-2.PNG)
- I use both checked on the picture
![alt text](./2-2-1.PNG)



### Module 3 — Prepare Source Documents
- Upload files to a container in Azure Storage:Container name: documents
![alt text](./3-1.PNG)

### Module 4 & 5 — Create the Search Index
- Option B — Better for learning: Create the index manually so students understand the schema.
![alt text](./4-1.PNG)

### Module 6 — Generate Embeddings and Load Documents
1.	Read document text
2.	Split into chunks
![alt text](./6-0-0.PNG)
3.	Call embedding model
![alt text](./6-0.PNG)
4.	Upload documents with vectors to Azure AI Search
![alt text](./6-1.PNG)

### Module 7 — Run Vector and Hybrid Search Queries
A. Keyword search
![alt text](./7-0-1.PNG)
B. Vector search
![alt text](./7-0-2.PNG)
C. Hybrid search
![alt text](./7-0-3.PNG)
- Ouputs
![alt text](./7-2.PNG)

### Module 8 — Add the LLM Layer
1.	User asks question
2.	Search index retrieves top 3–5 chunks
3.	Construct prompt with context
4.	Send prompt to chat model
5.	Return answer with sources
![alt text](./8-0.PNG)
