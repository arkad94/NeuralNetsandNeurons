import os
import json
import requests
import re
from openai import OpenAI

client = OpenAI()

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")


def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "words": "Give 5 words in Japanese based on the tag given, Make sure you tabulate them as Japanese word, Furigana, English word, and example sentence in respective columns",
        "story": "Write a story in japanese length of which is between 3000-4000 characters, followed with a summary in English and in the end under the header difficult words tabulate difficult Japanese words and their english translations. Japanese Story has heading as title, the english summary which follows the Japanese story has title English Summary, and the difficult words are under the header difficult words as (日本語・English Pronounciation) devation from the format would be harmful",
        # Add more CMDs and their templates here
    }

    prompt_template = cmd_templates.get(CMD, "CMD not recognized. Please enter a valid CMD, Please refer to the table above and enter exact CMD case sensitive..")
    instructions = []

    if tag:
        instructions.append(f"Tag: {tag}")
    if SPINS.strip():
        instructions.append(f"SPINS: {SPINS.strip()}")

    instruction_str = ", ".join(instructions)
    final_prompt = f"{prompt_template} based on the following instructions: {instruction_str}." if instructions else prompt_template
    return final_prompt, CMD in cmd_templates
    

def generate_image_with_dalle(story):
    # Initialize OpenAI client
    client = OpenAI()

    # Truncate the story to the first 4000 characters
    truncated_story = story[:4000]

    # Prepare the prompt for DALL-E
    dalle_prompt = "Generate an image that visually represents this story: \"" + truncated_story + "\". Please do not include any text in the image."

    # Make the API request to DALL-E
    response = client.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Check if the response contains the image data
    if response.data and len(response.data) > 0:
        image_url = response.data[0].url
        return image_url
    else:
        print(f"Error in image generation: {response.error}")
        return ""

def extract_words(response_text):
    # Implement the logic to parse the response_text and extract words
    # This is a placeholder function; adjust the parsing logic based on the actual response format
    words = []
    # ... parsing logic to fill the words list ...
    return words

def process_text(text):
    # Regular expression patterns
    japanese_pattern = r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]+'
    english_pattern = r'[A-Za-z0-9\s,.;\'"-]+'
    
    # Extract Japanese and English text
    japanese_story = ' '.join(re.findall(japanese_pattern, text))
    english_summary = ' '.join(re.findall(english_pattern, text))

    # Find the difficult words section
    difficult_words_section = re.search('Difficult Words(.*)', text, re.DOTALL)

    # Initialize an empty list to store formatted difficult words
    formatted_difficult_words = []

    if difficult_words_section:
        # Extract the difficult words from the section
        difficult_words_lines = difficult_words_section.group(1).strip().split('\n')
        for line in difficult_words_lines:
            # Split the line using the middle dot as the delimiter
            parts = line.split('・')
            if len(parts) == 2:
                japanese = parts[0].strip()
                english = parts[1].strip()
                formatted_difficult_words.append({'japanese': japanese, 'english': english})

    return japanese_story, english_summary, formatted_difficult_words



def send_prompt_to_openai(CMD, tag, SPINS):
    final_prompt, valid_cmd = create_prompt(CMD, tag, SPINS)
    if valid_cmd:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo-1106",
            "messages": [{"role": "user", "content": final_prompt}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                                 headers=headers, 
                                 data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            text_response = response_data['choices'][0]['message']['content'].strip()
            return text_response
        else:
            print("Error:", response.status_code, response.text)
            return ""

    return ""


def extract_difficult_words(response):
    # First, isolate the difficult words section
    difficult_words_section = response.split('Difficult Words')[1] if 'Difficult Words' in response else ""
    
    difficult_words = []
    # Now process each line within this section
    for line in difficult_words_section.split('\n'):
        if '・' in line:  # Correct delimiter for splitting
            parts = line.strip().split('・')  # Split using the correct delimiter
            if len(parts) == 2:
                japanese, english = parts[0], parts[1]
                difficult_words.append({'japanese': japanese.strip(), 'english': english.strip()})
    return difficult_words
