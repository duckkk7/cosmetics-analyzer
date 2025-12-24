import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)


def ask_llm(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct:together",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=3000,
            temperature=0.7,
            top_p=0.9,
            stream=False
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Ошибка LLM: {str(e)}"
