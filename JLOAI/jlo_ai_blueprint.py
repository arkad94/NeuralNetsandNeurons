
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_socketio import  emit
from dbextension import db
from db_operations import add_user, get_users, add_word, get_words, update_word, delete_word
from prompter import send_prompt_to_openai, generate_image_with_dalle, process_text, extract_difficult_words
from models import  User, Word

jlo_ai_blueprint = Blueprint('jlo_ai', __name__)


db.init_app(jlo_ai_blueprint.route)


@jlo_ai_blueprint.route('/prompter', methods=['GET'])
def prompter():
    # Render the prompter form
    return render_template('prompter_form.html')



@socketio.on('send_prompt')
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





@jlo_ai_blueprint.route('/add_user', methods=['GET', 'POST'])
def route_add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        response = add_user(username, email)
        return jsonify({'message': response})
    return render_template('add_user.html')

@jlo_ai_blueprint.route('/users', methods=['GET'])
def route_get_users():
    users = get_users()
    return render_template('users.html', users=users)

@jlo_ai_blueprint.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def route_update_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('route_get_users'))
    return render_template('update_user.html', user=user)

@jlo_ai_blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
def route_delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('route_get_users'))

@jlo_ai_blueprint.route('/add_word', methods=['GET', 'POST'])
def route_add_word():
    if request.method == 'POST':
        japanese = request.form['japanese']
        english = request.form['english']
        response = add_word(japanese, english)
        return jsonify({'message': response})
    return render_template('add_word.html')

@jlo_ai_blueprint.route('/get_words', methods=['GET'])
def route_get_words():
    words = get_words()
    return render_template('get_words.html', words=words)

@jlo_ai_blueprint.route('/update_word/<int:word_id>', methods=['GET', 'POST'])
def route_update_word(word_id):
    word = Word.query.get(word_id)
    if request.method == 'POST':
        word.japanese = request.form['japanese']
        word.english = request.form['english']
        db.session.commit()
        return redirect(url_for('route_get_words'))
    return render_template('update_word.html', word=word)

@jlo_ai_blueprint.route('/delete_word/<int:word_id>', methods=['POST'])
def route_delete_word(word_id):
    word = Word.query.get(word_id)
    db.session.delete(word)
    db.session.commit()
    return redirect(url_for('route_get_words'))

@jlo_ai_blueprint.cli.command('create_db')
def create_db():
    db.create_all()
    print("Database tables created.")


