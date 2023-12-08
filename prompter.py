import os
from openai import OpenAI

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

messages = [{"role": "system", "content": "You are a japanese language teacher"}]

def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "Word of The Day in Japanese": "Give 5 words in Japanese based on the tag given,tabulate them as Japanese word,Furigana,English word,example sentence in respective columns",
        "A Story": "Give a story in Japanese according to tag, beginner level and also seperately list the difficult words in furigana, finally summarise the story in english as well",
        # Add more CMDs and their templates here
    }

    prompt_template = cmd_templates.get(CMD, "Default template if CMD not found")

    # Combine your CMD, tag, and SPINS into a single instruction string
    instruction = f"CMD: {CMD}, Tag: {tag}, SPINS: {SPINS}"

    # Modify the prompt to include a summary request
    final_prompt = f"First, summarize the following instructions: {instruction}. Now, {prompt_template}."

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


