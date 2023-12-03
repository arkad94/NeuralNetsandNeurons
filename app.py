from flask import Flask, jsonify, request
from models import db
from admin import (add_user, get_users, update_user, delete_user, 
                   add_word, get_words, update_word, delete_word,
                   add_tag, get_tags, update_tag, delete_tag)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jlo_ai.db'
db.init_app(app)

@app.route('/')
def index():
    return 'Flask is Working!'

# CRUD routes for User
@app.route('/add_user/<username>/<email>', methods=['POST'])
def route_add_user(username, email):
    add_user(username, email)
    return jsonify({'message': 'User added'})

@app.route('/users', methods=['GET'])
def route_get_users():
    # This function fetches users from the database and constructs a list of dictionaries
    # with both the user's ID and username before returning it as a JSON response.
    users = get_users()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify({'users': users_list})

@app.route('/update_user/<int:user_id>/<username>/<email>', methods=['PUT'])
def route_update_user(user_id, username, email):
    result = update_user(user_id, username, email)
    return jsonify({'message': 'User updated' if result else 'User not found'})

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def route_delete_user(user_id):
    result = delete_user(user_id)
    return jsonify({'message': 'User deleted' if result else 'User not found'})

# CRUD routes for Word
@app.route('/add_word', methods=['POST'])
def route_add_word():
    data = request.json
    japanese = data.get('japanese')
    english = data.get('english')
    add_word(japanese, english)
    return jsonify({'message': 'Word added'})

@app.route('/words', methods=['GET'])
def route_get_words():
    words = get_words()
    words_list = [{'id': word.id, 'japanese': word.japanese, 'english': word.english} for word in words]
    return jsonify({'words': words_list})

@app.route('/update_word/<int:word_id>', methods=['PUT'])
def route_update_word(word_id):
    data = request.json
    new_japanese = data.get('japanese')
    new_english = data.get('english')
    result = update_word(word_id, new_japanese, new_english)
    return jsonify({'message': 'Word updated' if result else 'Word not found'})

@app.route('/delete_word/<int:word_id>', methods=['DELETE'])
def route_delete_word(word_id):
    result = delete_word(word_id)
    return jsonify({'message': 'Word deleted' if result else 'Word not found'})

# CRUD routes for Tag
@app.route('/add_tag', methods=['POST'])
def route_add_tag():
    data = request.json
    name = data.get('name')
    add_tag(name)
    return jsonify({'message': 'Tag added'})

@app.route('/tags', methods=['GET'])
def route_get_tags():
    tags = get_tags()
    tags_list = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return jsonify({'tags': tags_list})

@app.route('/update_tag/<int:tag_id>', methods=['PUT'])
def route_update_tag(tag_id):
    data = request.json
    new_name = data.get('name')
    result = update_tag(tag_id, new_name)
    return jsonify({'message': 'Tag updated' if result else 'Tag not found'})

@app.route('/delete_tag/<int:tag_id>', methods=['DELETE'])
def route_delete_tag(tag_id):
    result = delete_tag(tag_id)
    return jsonify({'message': 'Tag deleted' if result else 'Tag not found'})

@app.cli.command('create_db')
def create_db():
    db.create_all()
    print("Database tables created.")

if __name__ == '__main__':
    app.run(debug=True)
