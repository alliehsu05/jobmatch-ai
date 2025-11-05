import os
from docx import Document

from LoggerManager import logger_manager


def get_resume_path(folder='resources'):
    for f in os.listdir(folder):
        if "resume" in f.lower() and f.lower().endswith(".docx"):
            return os.path.join(folder, f)
    logger_manager.error(
        f"No DoCX file containing 'resume' found in '{folder}' folder.",
        True,
        FileNotFoundError
    )

def read_resume(path):
    """
    Read .docx resume and return plain text.
    """
    try:
        doc = Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        if not text.strip():
            logger_manager.error(
                "Resume file is empty or unreadable.",
                True,
                ValueError
            )
        return text
    except Exception as err:
        logger_manager.error(
            f"Failed to read DOCX file: {err}",
            True
        )

if __name__ == '__main__':
    resume_path = get_resume_path()
    resume_text = read_resume(resume_path)
    print(resume_text)
