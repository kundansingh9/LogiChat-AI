from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from rag import process_pdf, ask_question
from research_agent import LogisticsResearcher

app = FastAPI()
researcher = LogisticsResearcher()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        import os
        os.makedirs("uploads", exist_ok=True)

        path = f"uploads/{file.filename}"

        with open(path, "wb") as f:
            f.write(await file.read())

        process_pdf(path)

        return {"message": "PDF Uploaded Successfully"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/chat")
def chat(query: str):
    answer = ask_question(query)
    return {"response": answer}

@app.get("/research")
def research(query: str):
    try:
        result = researcher.research(query)
        return result
    except Exception as e:
        return {"error": str(e)}