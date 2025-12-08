import streamlit as st

from jobmatch_core import run_jobmatch


st.set_page_config(page_title="JobMatch.ai Demo", layout="wide")
st.title("Welcome to JobMatch.ai")

# set left sidebar
st.sidebar.header("Resume & Job Descriptions")
resume_text = st.sidebar.text_area("Paste your resume text here:", height=200)

jd_entries = {}
for i in range(1, 4):
    title = st.sidebar.text_input(f"Job {i} Title", key=f"title_{i}")
    jd = st.sidebar.text_area(f"Job {i} Description", height=150, key=f"jd_{i}")
    if title.strip() and jd.strip():
        jd_entries[title.strip()] = jd.strip()

run_button = st.sidebar.button("🚀 Run Match")

if run_button:
    if not resume_text:
        st.error("Please enter your Resume.")
    elif not jd_entries:
        st.error("Please enter at least one Job Description")
    else:
        df = run_jobmatch(resume_text, jd_entries)

        st.subheader("📊 Job Match Results")

        for _, row in df.iterrows():
            st.markdown("---")
            st.markdown(f"### {row['Job Title']}")
            st.markdown(f"**Match Score:** {row['Match Score']}")
            st.markdown(f"**Strength:** {row['Strength']}")
            st.markdown(f"**Weakness:** {row['Weakness']}")
            st.markdown("**Summary:**")
            st.info(row["Summary"])
