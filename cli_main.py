from jd_reader import get_jd_path, read_jd
from resume_reader import get_resume_path, read_resume
from jobmatch_core import run_jobmatch

if __name__ == "__main__":
    resume_text = read_resume(get_resume_path())
    jd_dict = read_jd(get_jd_path())

    df = run_jobmatch(resume_text, jd_dict)
    print(df.to_string(index=False))
