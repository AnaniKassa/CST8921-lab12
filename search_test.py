import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

load_dotenv()

# OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

# Search
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# -----------------------------
# Keyword Search
# -----------------------------
print("\n=== KEYWORD SEARCH ===")

results = search_client.search(
    search_text="vacation days"
)

for r in results:
    print(r["content"])

# -----------------------------
# Vector Search
# -----------------------------
def get_embedding(text):
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL_DEPLOYMENT"),
        input=text
    )
    return response.data[0].embedding

print("\n=== VECTOR SEARCH ===")

query = "How many vacation days do I get?"
vector = get_embedding(query)

results = search_client.search(
    search_text=None,
    vector_queries=[{
        "kind": "vector",
        "vector": vector,
        "k": 3,
        "fields": "contentVector"
    }]
)


for r in results:
    print(r["content"])

# -----------------------------
# Hybrid Search
# -----------------------------
print("\n=== HYBRID SEARCH ===")

results = search_client.search(
    search_text="vacation policy",
    vector_queries=[{
        "kind": "vector",
        "vector": vector,
        "k": 3,
        "fields": "contentVector"
    }]
)

for r in results:
    print(r["content"])

# -----------------------------
# 8.1 — Add function
# -----------------------------
def ask_llm(question, context_chunks):
    context = "\n\n".join(context_chunks)

    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You answer only from provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return response.choices[0].message.content

# -----------------------------
# 8.2 — Retrieve context
# -----------------------------
print("\n=== RAG QUESTION ===")

question = "How many vacation days after 5 years?"

vector = get_embedding(question)

results = search_client.search(
    search_text=question,
    vector_queries=[{
        "kind": "vector",
        "vector": vector,
        "k": 3,
        "fields": "contentVector"
    }]
)


chunks = [r["content"] for r in results]

answer = ask_llm(question, chunks)

print("\nFinal Answer:\n", answer)
