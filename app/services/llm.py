import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


def generate_answer(question: str, context: str) -> str:
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN is not set")

    client = InferenceClient(
        model=MODEL_NAME,
        provider="auto",
        api_key=HF_TOKEN,
    )

    prompt = f"""You are a space intelligence assistant.

Answer the question using ONLY the provided context.
If the context does not contain enough information, say:
"I don't have enough information in the knowledge base to answer this."

Context:
{context}

Question:
{question}
"""

    response = client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "Answer accurately using only the supplied context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=150,
        temperature=0.2,
    )

    return response.choices[0].message.content