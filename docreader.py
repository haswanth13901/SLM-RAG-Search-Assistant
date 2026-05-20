import fitz
import os

MAX_FILE_SIZE_MB = 2
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_md(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text(file_obj):
    if file_obj is None:
        return None, None

    if hasattr(file_obj, 'name'):
        file_path = file_obj.name
    else:
        file_path = file_obj

    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE_BYTES:
        size_in_mb = file_size / (1024 * 1024)
        return None, f"File too large ({size_in_mb:.1f} MB). Maximum allowed size is {MAX_FILE_SIZE_MB} MB. Please upload a smaller file."

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf" or ext == "":
        try:
            return read_pdf(file_path), None
        except Exception:
            pass

    if ext in (".txt", ".md", ""):
        try:
            return read_txt(file_path), None
        except Exception:
            pass

    return None, "Unsupported file type. Please upload a PDF, TXT, or MD file."