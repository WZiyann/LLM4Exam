from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag import search_similar_questions
from generator import generate_questions
from docgen import generate_word_doc
import uuid, os

app = FastAPI()

class GenerationRequest(BaseModel):
    subject: str
    grade: str
    question_type: str
    count: int
    prompt: str

@app.post("/generate")
def generate_exam(request: GenerationRequest):
    context = search_similar_questions(request.prompt)
    questions = generate_questions(request.prompt, context, request.count)
    doc_path = generate_word_doc(questions, request.subject)
    return {"file": doc_path}

@app.get("/download")
def download_file(path: str):
    return FileResponse(path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=os.path.basename(path))
