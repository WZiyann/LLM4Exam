from docx import Document
import os, uuid

def generate_word_doc(questions_str, subject):
    doc = Document()
    doc.add_heading(f"{subject} 试卷", 0)
    for line in questions_str.split("\n"):
        doc.add_paragraph(line)
    filename = f"/tmp/{uuid.uuid4()}.docx"
    doc.save(filename)
    return filename
