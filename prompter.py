import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "Word of The Day in Japanese": "Template for command 1",
        "A Story": "Template for command 2",
        # Add more CMDs and their templates here
    }
    
    prompt_template = cmd_templates.get(CMD, "Default template if CMD not found")
    final_prompt = f"{prompt_template} with Tag: {tag} and Additional Instructions: {SPINS}"
    return final_prompt

final_prompt = create_prompt("A Story", "Technology", "Include examples")

# Make the API call using the generated prompt
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": final_prompt}
    ],
    model="gpt-4",
)

print(chat_completion.choices[0].message.content)



