import pandas as pd

from gpt_utils import safe_api_call, parse_gpt_json
from nlp_utils import extract_key_sentences


def run_jobmatch(resume_text, jd_dict):
    # preprocess resume
    processed_resume = extract_key_sentences(resume_text)

    # preprocess job description
    processed_jd_dict = {
        title: extract_key_sentences(jd) for title, jd in jd_dict.items()
    }
    jd_prompt_section = "\n\n".join(f"[Job Title]\n{title}\n[JD]\n{jd}" for title, jd in processed_jd_dict.items())

    # construct prompt
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

    # convert to table
    scores_df = pd.DataFrame([
        {
            "Job Title": match_result["job_title"],
            "Match Score": match_result["match_score"],
            "Strength": ", ".join(match_result["strength"]),
            "Weakness": ", ".join(match_result["weakness"]),
            "Summary": match_result["summary"],
        }
        for match_result in json_completion
    ])

    # sort by match score (descending)
    scores_df = scores_df.sort_values(by="Match Score", ascending=False)

    return scores_df
