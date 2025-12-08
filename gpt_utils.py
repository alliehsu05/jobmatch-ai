import json
import os
import time

from openai import OpenAI, OpenAIError

from LoggerManager import logger_manager
from token_utils import count_tokens

REQUIRED_KEYS = {"job_title", "match_score", "strength", "weakness", "summary"}


# load API key
def load_api_key():
    """
    Priority:
    1. Streamlit Cloud secrets
    2. .env file in local
    """
    try:
        import streamlit as st
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass # not in Streamlit environment

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

    return os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=load_api_key())

def _call_gpt(prompt):
    """
    Direct GPT API call.
    """
    return client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o",
        max_tokens=1000
    )

def monitor_api_performance(func):
    """
    Decorator to wrap API calls with latency and token logging.
    """
    def wrapper(*args, **kwargs):
        # Assume prompt is first positional arg or in kwargs
        prompt = kwargs.get("prompt") or (args[0] if args else "")
        tokens = count_tokens(prompt)
        start = time.time()
        try:
            result = func(*args, **kwargs)  # call the original function
            latency = time.time() - start
            logger_manager.info(f"API Call Success | Tokens counts: {tokens}, Latency: {latency:.2f}s")
            return result
        except Exception as e:
            latency = time.time() - start
            logger_manager.error(
                f"API Call Failure | Latency: {latency:.2f}s | Error: {e}",
                True,
                type(e))
    return wrapper

@monitor_api_performance
def safe_api_call(prompt, retries=2, delay=2):
    """
    Safe GPT API call with basic retry and error logging.
    """
    for attempt in range(1, retries + 1):
        try:
            completion = _call_gpt(prompt)
            return completion.choices[0].message.content
        except (OpenAIError, ValueError) as e:
            logger_manager.warning(f"Attempt {attempt} failed: {e}")
            time.sleep(delay)
    logger_manager.error(
        "API call failed after retries",
        True
    )

def parse_gpt_json(content, required_keys=REQUIRED_KEYS):
    """
    Parse GPT response content as JSON.
    """
    try:
        objects = json.loads(content.replace("```json", "").replace("```", "").strip())["results"]
        for i, obj in enumerate(objects, start=1):
            missing_keys = required_keys - obj.keys()
            if missing_keys:
                raise ValueError(f"Object {i} is missing keys: {missing_keys}")
        return objects
    except json.decoder.JSONDecodeError as e:
        logger_manager.error(f"JSON parsing error: {e}", True, ValueError)
    except ValueError as ve:
        logger_manager.error(f"{ve}", True, type(ve))
