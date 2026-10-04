from pathlib import Path
from pypdf import PdfReader

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(filename, content):
    path = UPLOAD_DIR / filename
    path.write_bytes(content)
    return path

def extract_pdf(path):
    reader = PdfReader(str(path))
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)
