import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAPI_API_KEY")
)

prompt = "Ready to dive into the job board ocean with me?"

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="gpt-4o",
    max_tokens=250
)

print(completion.choices[0].message.content)
