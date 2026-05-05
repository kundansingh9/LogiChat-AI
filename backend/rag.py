import chromadb
import requests
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import uuid
from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


# Vector DB
client = chromadb.PersistentClient(path="chroma_db")
# Collection name
COLLECTION_NAME = "logistics_docs"
collection = client.get_or_create_collection(name=COLLECTION_NAME)

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





def process_pdf(path):
    # 1. Clear old data (User wants to chat with the current document)
    global collection
    try:
        client.delete_collection(name=COLLECTION_NAME)
        collection = client.create_collection(name=COLLECTION_NAME)
        print(f"Collection {COLLECTION_NAME} reset.")
    except Exception as e:
        print(f"Error resetting collection: {e}")

    # 2. Extract text
    text = extract_text(path)
    
    # 3. Use Recursive Splitter for better context preservation
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    print(f"Split document into {len(chunks)} chunks.")

    # 4. Batch add for performance
    ids = [str(uuid.uuid4()) for _ in chunks]
    embeddings = model.encode(chunks).tolist()
    
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )
    print("Successfully added chunks to ChromaDB.")


def ask_question(query):
    try:
        query_embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5  # Increased context window
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