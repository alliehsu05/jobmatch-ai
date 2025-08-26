import os

def get_jd_path(folder='resources'):
    jd_path = []

    for f in os.listdir(folder):
        if f.lower().endswith(".txt"):
            jd_path.append(os.path.join(folder, f))

    if jd_path:
        return jd_path
    raise FileNotFoundError(f"No TEXT file found in '{folder}' folder.")

def read_jd(paths):
    """
    Read job description files and return a dictionary:
    {job_title: text_content}
    """
    jd_text = {}
    for path in paths:
        job_title = os.path.basename(path)
        try:
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            jd_text[job_title] = text
        except Exception as err:
            raise RuntimeError(f"Failed to read TEXT file {job_title}: {err}")
    return jd_text

if __name__ == '__main__':
    jd_path = get_jd_path()
    jd_text = read_jd(jd_path)
    print(jd_text)
