from pathlib import Path

def create_audio(text, filename="audio.mp3"):
    # Dummy audio creation so app starts
    # Creates empty file in uploads
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    path = upload_dir / filename
    path.write_bytes(b"")  # empty for now
    return str(path)

def text_to_speech(text):
    return create_audio(text)