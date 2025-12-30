from PyPDF2 import PdfReader
from docx import Document
import os

def convert(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.pdf':
        reader = PdfReader(input_path)
        with open(output_path, "w") as f:
            for page in reader.pages:
                f.write(page.extract_text() or "")
    elif ext == '.docx':
        doc = Document(input_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        with open(output_path, "w") as f:
            f.write(text)
