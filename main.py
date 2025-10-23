import os
from dotenv import load_dotenv
from openai import OpenAI

from jd_reader import get_jd_path, read_jd
from nlp_utils import extract_key_sentences
from resume_reader import get_resume_path, read_resume
from token_utils import count_tokens


# load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAPI_API_KEY"))

# read and preprocess resume
resume_path = get_resume_path()
resume_text = read_resume(resume_path)
processed_resume = extract_key_sentences(resume_text)

# read and preprocess job description
jd_paths = get_jd_path()
jd_dict = read_jd(jd_paths)
processed_jd_dict = {title: extract_key_sentences(jd) for title, jd in jd_dict.items()}
jd_prompt_section = "\n\n".join(f"[Job Title]\n{title}\n[JD]\n{jd}" for title, jd in processed_jd_dict.items())

# Construct prompt
prompt = f"""
### Identity
You are a senior recruiter specializing in software engineer roles.

### Instructions
Compare the candidate's resume with each job description provided.
Return a JSON with a top-level key "results", which is a list of objects.
Each object must contain exactly these keys:
- job_title
- match_score (0-10)
- strengths (array of strings)
- weakness (array of strings)
- summary (concise actionable advice)

### Context
[Resume]
{processed_resume}

==============================
{jd_prompt_section}
"""

print(prompt)
print("Tokens", count_tokens(prompt))

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="gpt-4o",
    max_tokens=1000
)

print(completion.choices[0].message.content)
