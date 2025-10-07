import os
from dotenv import load_dotenv
from openai import OpenAI

from resume_reader import get_resume_path, read_resume
from jd_reader import get_jd_path, read_jd
from token_utils import count_tokens


# load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAPI_API_KEY"))


# read resume and job description
resume_path = get_resume_path()
resume_text = read_resume(resume_path)

jd_paths = get_jd_path()
jd_text = read_jd(jd_paths)


# Construct prompt
prompt = f"""
This is a candidate's resume along with multiple job descriptions.
Please analyze the candidate's suitability, skill match, and potential gaps, then provide a brief summary and suitability rating for each position.

[Resume]
{resume_text}

==============================
"""

for title, jd in jd_text.items():
    prompt += f"\n\n[Job Title: {title}]\n\n{jd}\n-"

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
