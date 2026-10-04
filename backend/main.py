from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from backend.services.document_service import save_file, extract_pdf
from backend.services.ai_service import ask_ai, generate_quiz, summarize
from backend.services.audio_service import create_audio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

current_document_text = ""

@app.get("/")
def home():
    return FileResponse(BASE_DIR/"frontend"/"index.html")
@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    global current_document_text
    path = save_file(file)
    text = extract_pdf(path)
    current_document_text = text
    return {"text": text[:2000] + "...", "filename": file.filename}

@app.post("/api/ask")
async def ask(question: str):
    global current_document_text
    if not current_document_text:
        return {"answer": "Please upload a PDF first!"}
    answer = ask_ai(current_document_text, question)
    return {"answer": answer}

@app.post("/api/quiz")
async def quiz():
    global current_document_text
    if not current_document_text:
        return {"quiz": "Please upload a PDF first!"}
    quiz_text = generate_quiz(current_document_text)
    return {"quiz": quiz_text}

@app.post("/api/summary")
async def summary():
    global current_document_text
    if not current_document_text:
        return {"summary": "Please upload a PDF first!"}
    summary_text = summarize(current_document_text)
    return {"summary": summary_text}

@app.post("/api/audio")
async def audio():
    global current_document_text
    if not current_document_text:
        return {"audio": ""}
    audio_path = create_audio(current_document_text[:4000])
    return {"audio": "/audio-file"}

@app.get("/audio-file")
def get_audio():
    return FileResponse("audio_output.mp3", media_type="audio/mpeg")

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/",
    StaticFiles(directory=BASE_DIR / "frontend", html=True),
    name="frontend",
)
