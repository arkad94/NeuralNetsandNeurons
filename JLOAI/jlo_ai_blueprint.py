
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_socketio import emit
from .prompter import send_prompt_to_openai, generate_image_with_dalle, process_text, extract_difficult_words
from extensions import socketio 

jlo_ai_blueprint = Blueprint('jlo_ai', __name__, template_folder='jloai')





@jlo_ai_blueprint.route('/prompter', methods=['GET'])
def prompter():
    # Render the prompter form
    return render_template('prompter_form.html')



@socketio.on('send_prompt', namespace='/jlo_ai')
def handle_send_prompt(data):
    CMD = data['CMD']
    tag = data['tag']
    SPINS = data['SPINS']

    response = send_prompt_to_openai(CMD, tag, SPINS)

    if CMD == "words":
        # Directly emit the OpenAI response for Word of The Day
        emit('prompt_response', {'openai_raw_response': response})
    elif CMD == "story":
        # Handle the streaming process for A Story
        japanese_story, english_summary, difficult_words = process_text(response)
        image_url = generate_image_with_dalle(english_summary)
        emit('prompt_response', {
            'japanese_story': japanese_story,
            'english_summary': english_summary,
            'difficult_words': difficult_words,
            'image_url': image_url
        })
    else:
        emit('prompt_response', {'error': "Invalid Command"})



