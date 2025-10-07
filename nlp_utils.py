import re
import spacy


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def clean_text(raw_text: str) -> str:
    # Remove disruptive symbols except sentence punctuation
    text = re.sub(r"[^\w\s\.\?\!]", " ", raw_text)
    # Remove extra spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()
    # Remove stopwords
    doc = nlp(text)
    cleaned_text = " ".join(
        token.text for token in doc if token.text.lower() not in nlp.Defaults.stop_words
    )

    return cleaned_text

def extract_skills(text: str) -> set:
    """
    Extract potential skill keywords from text using spaCy.
    Grabs all NOUNs and PROPNs.
    Returns a set of unique skills.
    """
    doc = nlp(text.lower())
    extracted_skills = {token.text for token in doc if token.pos_ in ("NOUN", "PROPN")}

    return extracted_skills

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
