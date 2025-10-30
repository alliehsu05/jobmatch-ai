import logging
import os
import time
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from token_utils import count_tokens


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAPI_API_KEY"))

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
            logging.info(f"API Call Success | Tokens counts: {tokens}, Latency: {latency:.2f}s")
            return result
        except Exception as e:
            latency = time.time() - start
            logging.error(f"API Call Failure | Latency: {latency:.2f}s | Error: {e}")
            raise
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
            logging.warning(f"Attempt {attempt} failed: {e}")
            time.sleep(delay)
    raise RuntimeError("API call failed after retries")
