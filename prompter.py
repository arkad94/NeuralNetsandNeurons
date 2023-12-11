import os
import json
import requests
from openai import OpenAI

client = OpenAI()

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")


def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "Word of The Day in Japanese": "Give 5 words in Japanese based on the tag given, Make sure you tabulate them as Japanese word, Furigana, English word, and example sentence in respective columns",
        "A Story": "Write a Japanese story in Japanese, with a summary in English following Japanese text separately listing difficult Japanese words used in the story in a tabulated format exactly as follows, no deviations tolerated: Japanese Word| English Translation, don't use brackets or empty space anywhere in your output",
        # Add more CMDs and their templates here
    }

    prompt_template = cmd_templates.get(CMD, "CMD not recognized. Please enter a valid CMD.")
    instructions = []

    if tag:
        instructions.append(f"Tag: {tag}")
    if SPINS.strip():
        instructions.append(f"SPINS: {SPINS.strip()}")

    instruction_str = ", ".join(instructions)
    final_prompt = f"{prompt_template} based on the following instructions: {instruction_str}." if instructions else prompt_template
    return final_prompt, CMD in cmd_templates


def send_prompt_to_openai(CMD, tag, SPINS, stream=False):
    final_prompt, valid_cmd = create_prompt(CMD, tag, SPINS)
    if valid_cmd:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": final_prompt}],
            "stream": stream  # Enable streaming if required
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", 
                                 headers=headers, 
                                 data=json.dumps(data))

        if response.status_code == 200:
            if not stream:
                # For non-streaming responses
                response_data = response.json()
                text_response = response_data['choices'][0]['message']['content'].strip()
                difficult_words = extract_difficult_words(text_response)
                return text_response, difficult_words
            else:
                # Handle streamed responses here
                for line in response.iter_lines():
                    if line:
                        streamed_response = json.loads(line.decode('utf-8'))
                        if 'choices' in streamed_response and 'delta' in streamed_response['choices'][0]:
                            delta_content = streamed_response['choices'][0]['delta'].get('content', '')
                            yield delta_content  # Yield the chunk for streaming
        else:
            print("Error:", response.status_code, response.text)
            return "", []

    return "", []




def extract_difficult_words(response):
    difficult_words = []
    for line in response.split('\n'):
        if '|' in line:  # Adjusted to match the new delimiter
            parts = line.strip().split('|')
            if len(parts) == 2:
                japanese, english = parts
                difficult_words.append((japanese.strip(), english.strip()))
    return difficult_words