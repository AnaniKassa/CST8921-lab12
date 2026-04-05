import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Load environment variables
load_dotenv()

# -----------------------------
# Azure AI Foundry (OpenAI client)
# -----------------------------
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

# -----------------------------
# Azure AI Search client
# -----------------------------
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# -----------------------------
# Function to generate embeddings
# -----------------------------
def get_embedding(text):
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL_DEPLOYMENT"),
        input=text
    )
    return response.data[0].embedding

# -----------------------------
# NEW: Chunking function
# -----------------------------
def chunk_text(text, chunk_size=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size
    return chunks

# -----------------------------
# Sample documents (still OK for lab)
# -----------------------------
documents = [
    {
        "id": "1",
        "title": "Vacation Policy",
        "content": "Employees receive 15 vacation days after 5 years.",
        "category": "HR",
        "sourceFile": "vacation-policy.txt"
    },
    {
        "id": "2",
        "title": "Remote Work Policy",
        "content": "Employees may work remotely up to 3 days per week.",
        "category": "HR",
        "sourceFile": "remote-work-policy.txt"
    },
    {
        "id": "3",
        "title": "Benefits Overview",
        "content": "The company provides health, dental, and vision insurance.",
        "category": "HR",
        "sourceFile": "benefits-overview.txt"
    }
]

# -----------------------------
# NEW: Chunk + embed + prepare upload
# -----------------------------
docs_to_upload = []

for doc in documents:
    print(f"Processing document: {doc['title']}")

    chunks = chunk_text(doc["content"])

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        docs_to_upload.append({
            "id": f"{doc['id']}-{i}",
            "title": doc["title"],
            "content": chunk,
            "category": doc["category"],
            "sourceFile": doc["sourceFile"],
            "contentVector": embedding
        })

# -----------------------------
# Upload
# -----------------------------
print("Uploading documents to Azure AI Search...")

result = search_client.upload_documents(docs_to_upload)

print("Upload completed!")
print(result)
