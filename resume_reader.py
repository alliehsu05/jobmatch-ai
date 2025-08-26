import os
from docx import Document


def get_resume_path(folder='resources'):
    for f in os.listdir(folder):
        if "resume" in f.lower() and f.lower().endswith(".docx"):
            return os.path.join(folder, f)
    raise FileNotFoundError(f"No DoCX file containing 'resume' found in '{folder}' folder.")

def read_resume(path):
    """
    Read .docx resume and return plain text.
    """
    try:
        doc = Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as err:
        raise RuntimeError(f"Failed to read DOCX file: {err}")


if __name__ == '__main__':
    resume_path = get_resume_path()
    resume_text = read_resume(resume_path)
    print(resume_text)
