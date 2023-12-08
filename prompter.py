import os
from openai import OpenAI

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

messages = [{"role": "system", "content": "You are a Japanese Teacher"}]

def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "Word of The Day in Japanese": "Give 5 words in Japanese based on the tag given, tabulate them as Japanese word, Furigana, English word, example sentence in respective columns",
        "A Story": "Give a story in Japanese according to tag, beginner level and also separately list the difficult words,list difficult Japanese words in a tabulated format as follows: 'Japanese Word, English Translation'. For example: 'にほんご, Japanese Language'",
        # Add more CMDs and their templates here
    }

    prompt_template = cmd_templates.get(CMD, "Default template if CMD not found")
    final_prompt = ""
    if CMD in cmd_templates:
        final_prompt += f"CMD: {CMD}"

    final_prompt += f", Tag: {tag}"
    if SPINS.strip():
        final_prompt += f", SPINS: {SPINS}"

    final_prompt = f"First, summarize the following instructions: {final_prompt}. Now, {prompt_template}."
    return final_prompt


    # Add CMD to the prompt only if it's a valid key in cmd_templates
    if CMD in cmd_templates:
        final_prompt += f"CMD: {CMD}"

    # Add Tag and SPINS to the prompt
    final_prompt += f", Tag: {tag}"
    if SPINS.strip():  # Include SPINS only if it contains content
        final_prompt += f", SPINS: {SPINS}"

    # Complete the prompt with a summary request and the selected template
    final_prompt = f"First, summarize the following instructions: {final_prompt}. Now, {prompt_template}."

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
        parts = line.strip().split(', ')
        if len(parts) == 2:
            japanese, english = parts
            difficult_words.append((japanese, english))
    return difficult_words


