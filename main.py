from gpt_utils import safe_api_call, parse_gpt_json
from jd_reader import get_jd_path, read_jd
from nlp_utils import extract_key_sentences
from resume_reader import get_resume_path, read_resume


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
- strength (array of strings)
- weakness (array of strings)
- summary (concise actionable advice)

### Context
[Resume]
{processed_resume}

==============================
{jd_prompt_section}
"""

completion = safe_api_call(prompt)
json_completion = parse_gpt_json(completion)

output = ""
for match_result in json_completion:
    output += (
        f"Job Title: {match_result['job_title']}\n"
        f"Match Score: {match_result['match_score']}\n"
        f"Strength: {', '.join(match_result['strength'])}\n"
        f"Weakness: {', '.join(match_result['weakness'])}\n"
        f"Summary: {match_result['summary']}\n"
        "----------------------------------------\n"
    )

print(output)
