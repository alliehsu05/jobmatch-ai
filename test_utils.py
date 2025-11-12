import pytest
import os
from types import SimpleNamespace

from gpt_utils import safe_api_call, parse_gpt_json
from jd_reader import get_jd_path, read_jd
from resume_reader import get_resume_path, read_resume

MOCK_RESPONSE = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='''
    ```json
    {
    "results": [
        {
        "job_title": "Quality Engineer - Automation",
        "match_score": 8,
        "strengths": [
            "Strong experience in test automation"
        ],
        "weakness": [
            "No specific experience with Cypress"
        ],
        "summary": "Goot fit"
        }
    ]
    }
    ```
'''))])

MOCK_RESPONSE_NOT_JSON = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='''
    ```json
    Not a JSON Content
    ```
'''))])

MOCK_RESPONSE_MISSING_KEYS = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='''
    ```json
    {
    "results": [
        {
        "job_title": "Quality Engineer - Automation",
        "match_score": 8
        }
    ]
    }
    ```
'''))])


# File Path Tests
def test_resume_file_exists():
    path = get_resume_path('resources')
    assert os.path.exists(path)
    assert path.endswith('.docx')

def test_resume_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_resume_path('non_existent_dir')

def test_jd_file_exists():
    path = get_jd_path('resources')
    assert os.path.exists(path[0])
    assert path[0].endswith('.txt')

def test_jd_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_jd_path('non_existent_dir')

# File Reading Tests
def test_read_resume_returns_text():
    text = read_resume(get_resume_path('resources'))
    assert isinstance(text, str)
    assert text.strip() # not empty

def test_read_jd_returns_dict():
    jd_info = read_jd(get_jd_path('resources'))
    assert isinstance(jd_info, dict)


def _set_mock(monkeypatch, mock_response):
    def mock_call(prompt):
        return mock_response
    monkeypatch.setattr("gpt_utils._call_gpt", mock_call)

# GPT API Mock Tests
def test_safe_api_call_success(monkeypatch):
    _set_mock(monkeypatch, MOCK_RESPONSE)
    result = safe_api_call("Test prompt")
    assert isinstance(result, str)

def test_safe_api_call_retries(monkeypatch):
    call_count = {"n": 0}
    def mock_call(prompt):
        call_count["n"] += 1
        if call_count["n"] < 2:
            raise ValueError("Temporary error")
        return MOCK_RESPONSE
    monkeypatch.setattr("gpt_utils._call_gpt", mock_call)

    result = safe_api_call("Test retry", retries=2)
    assert isinstance(result, str)
    assert call_count["n"] == 2

def test_safe_api_call_retries_exceed(monkeypatch):
    call_count = {"n": 0}
    def mock_call(prompt):
        call_count["n"] += 1
        raise ValueError("Temporary error")
    monkeypatch.setattr("gpt_utils._call_gpt", mock_call)

    with pytest.raises(RuntimeError):
        safe_api_call("Test retry", retries=2)

def test_parse_gpt_json(monkeypatch):
    _set_mock(monkeypatch, MOCK_RESPONSE)
    completion = safe_api_call("Test Parse JSON")
    json_completion = parse_gpt_json(completion)
    assert isinstance(json_completion, list)
    assert json_completion[0]["job_title"] == "Quality Engineer - Automation"

def test_parse_gpt_json_invalid(monkeypatch):
    _set_mock(monkeypatch, MOCK_RESPONSE_NOT_JSON)
    completion = safe_api_call("Test prompt with invalid JSON")
    with pytest.raises(ValueError, match="JSON parsing error"):
        parse_gpt_json(completion)

def test_parse_gpt_json_missing_keys(monkeypatch):
    _set_mock(monkeypatch, MOCK_RESPONSE_MISSING_KEYS)
    completion = safe_api_call("Test prompt reponse with missing keys")
    with pytest.raises(ValueError, match="is missing keys"):
        parse_gpt_json(completion)
