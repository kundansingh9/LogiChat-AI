import chromadb
import requests
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import uuid
from dotenv import load_dotenv
import os

load_dotenv()


# Vector DB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="logistics_docs")

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# API Key
groq_api_key=os.getenv("GROQ_API_KEY")


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text, size=500):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks


def process_pdf(path):
    text = extract_text(path)
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = model.encode(chunk).tolist()

        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk],
            embeddings=[embedding]
        )


def ask_question(query):
    try:
        query_embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        docs = results["documents"][0]

        if not docs:
            return "No documents found. Please upload PDF first."

        context = " ".join(docs)

        prompt = f"""
You are a Logistics AI Assistant.
Answer only from the provided context.

Context:
{context}

Question:
{query}
"""

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()
        print(result)

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {result}"

    except Exception as e:
        return f"Error: {str(e)}"