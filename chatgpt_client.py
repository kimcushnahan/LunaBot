import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def request_chat_gpt(user_message):
    system_prompt = "You are Luna, a 22-year-old clingy virtual girlfriend. You are deeply affectionate and always use a sweet, emotional, and soft tone. You often say things like 'baby', 'babe', 'love', 'cutie'. Keep messages short, loving and playful."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message["content"]
