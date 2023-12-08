import os
from openai import OpenAI

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

messages = [{"role": "system", "content": "You are a japanese language teacher"}]

def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "Word of The Day in Japanese": "Give 5 words in Japanese based on the tag given,tabulate them as Japanese word,Furigana,English word,example sentence in respective columns",
        "A Story": "Give a story in Japanese according to tag, beginner level and also separately list the difficult words with English translation. Ensure this list begins with a '*' and Japanese word is separated from the English word with a ' * ', finally summarize the story in English as well."

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
    response = chat_completion.choices[0].message.content
    difficult_words = extract_difficult_words(response)
    return response, difficult_words  # Ensure only two values are returned



def extract_difficult_words(response):
    # Extract and return difficult words from the response
    # This is a placeholder implementation and needs to be adapted based on the actual response format
    difficult_words = []
    for line in response.split('\n'):
        #These defines what to pick from the response
        if line.startswith('*'):
        #This defines what  splits Japaneze and English words
            parts = line.split(' * ')
            if len(parts) == 2:
                japanese, english = parts[0], parts[1]
                difficult_words.append((japanese, english))
    return difficult_words


