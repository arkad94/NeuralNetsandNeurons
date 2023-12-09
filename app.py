from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, User, Word
from db_operations import add_user, get_users, update_user, delete_user, add_word, get_words, update_word, delete_word
from prompter import send_prompt_to_openai 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jlo_ai.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)


# Clear the Jinja2 cache
app.jinja_env.cache = {}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompter', methods=['GET', 'POST'])
def prompter():
    if request.method == 'POST':
        # Get the form data
        CMD = request.form.get('CMD')
        tag = request.form.get('tag')
        SPINS = request.form.get('SPINS')
        
        # Use the send_prompt_to_openai function to get the response and difficult words
        response, difficult_words = send_prompt_to_openai(CMD, tag, SPINS)
        
        # Redirect to a new template with the results
        return render_template('prompter_results.html', response=response, difficult_words=difficult_words)
    
    # If it's a GET request, just render the prompter form
    return render_template('prompter_form.html')
                           

@app.route('/add_user', methods=['GET', 'POST'])
def route_add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        response = add_user(username, email)
        return jsonify({'message': response})
    return render_template('add_user.html')

@app.route('/users', methods=['GET'])
def route_get_users():
    users = get_users()
    return render_template('users.html', users=users)

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def route_update_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('route_get_users'))
    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def route_delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('route_get_users'))

@app.route('/add_word', methods=['GET', 'POST'])
def route_add_word():
    if request.method == 'POST':
        japanese = request.form['japanese']
        english = request.form['english']
        response = add_word(japanese, english)
        return jsonify({'message': response})
    return render_template('add_word.html')

@app.route('/get_words', methods=['GET'])
def route_get_words():
    words = get_words()
    return render_template('get_words.html', words=words)

@app.route('/update_word/<int:word_id>', methods=['GET', 'POST'])
def route_update_word(word_id):
    word = Word.query.get(word_id)
    if request.method == 'POST':
        word.japanese = request.form['japanese']
        word.english = request.form['english']
        db.session.commit()
        return redirect(url_for('route_get_words'))
    return render_template('update_word.html', word=word)

@app.route('/delete_word/<int:word_id>', methods=['POST'])
def route_delete_word(word_id):
    word = Word.query.get(word_id)
    db.session.delete(word)
    db.session.commit()
    return redirect(url_for('route_get_words'))

@app.cli.command('create_db')
def create_db():
    db.create_all()
    print("Database tables created.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

