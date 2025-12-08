import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download("punkt")       # tokenizer
nltk.download('punkt_tab')
nltk.download("stopwords")   # stopwords
stop_words = set(stopwords.words("english"))


def clean_text(raw_text: str) -> str:
    # Remove disruptive symbols except sentence punctuation
    text = re.sub(r"[^\w\s\.\?\!]", " ", raw_text)
    # Remove extra spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()
    # Remove stopwords
    tokens = word_tokenize(text)
    cleaned_tokens = [w for w in tokens if w.lower() not in stop_words]
    return " ".join(cleaned_tokens)

def extract_skills(text: str) -> set:
    tokens = word_tokenize(text)
    skills = set()

    for t in tokens:
        if len(t) < 3:
            continue

        # Tech-style tokens (AWS, SQL, API, NodeJS)
        if t.isupper():
            skills.add(t)
            continue

        # CamelCase (PowerShell, PyTorch)
        if re.match(r"[A-Z][a-z]+[A-Z][a-z]+", t):
            skills.add(t)
            continue

        # Keep tokens that look like skill words
        if t[0].isalpha() and t.lower() not in stop_words:
            skills.add(t)

    return skills

def extract_key_sentences(text: str) -> str:
    """
    Keep only sentences that mention any skill from skills set.
    """
    cleaned_text = clean_text(text)
    extracted_skills = extract_skills(cleaned_text)

    # Split text into sentences
    sentences = re.split(r"(?<=[\.\?\!])\s+", cleaned_text)

    key_sentences = []
    for sentence in sentences:
        if any(skill.lower() in sentence.lower() for skill in extracted_skills):
            key_sentences.append(sentence)

    return " ".join(key_sentences)
