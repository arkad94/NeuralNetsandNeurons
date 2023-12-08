import os
from openai import OpenAI

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

messages = [{"role": "system", "content": "You are a Japanese Teacher."}]

def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "Word of The Day in Japanese": "Template for command 1",
        "A Story": "Template for command 2",
        # Add more CMDs and their templates here
    }
    prompt_template = cmd_templates.get(CMD, "Default template if CMD not found")
    final_prompt = f"{prompt_template} with Tag: {tag} and Additional Instructions: {SPINS}"
    return final_prompt

def send_prompt_to_openai(CMD, tag, SPINS):
    final_prompt = create_prompt(CMD, tag, SPINS)
    messages = [
        {"role": "user", "content": final_prompt}
    ]
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    return chat_completion.choices[0].message.content


