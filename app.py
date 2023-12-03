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
    # Endpoint for checking if the Flask app is running
    return 'Flask is Working!'

# CRUD routes for User
@app.route('/add_user/<username>/<email>', methods=['POST'])
def route_add_user(username, email):
    # Adds a new user with the provided username and email
    add_user(username, email)
    return jsonify({'message': 'User added'})
    # Example URL: POST http://localhost:5000/add_user/<username>/<email>

@app.route('/users', methods=['GET'])
def route_get_users():
    # Retrieves a list of all users with their IDs and usernames
    users = get_users()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify({'users': users_list})
    # Example URL: GET http://localhost:5000/users

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def route_update_user(user_id):
    data = request.json
    username = data.get('username')
    email = data.get('email')

    # Here you can call your update function
    # For now, you might not have extensive validation
    result = update_user(user_id, username, email)
    #Study integration with filter in project notebook for future implimentation

    return jsonify({'message': 'User updated' if result else 'User not found'})


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def route_delete_user(user_id):
    # Deletes a user based on their user ID
    result = delete_user(user_id)
    return jsonify({'message': 'User deleted' if result else 'User not found'})
    # Example URL: DELETE http://localhost:5000/delete_user/<user_id>

# CRUD routes for Word
@app.route('/add_word', methods=['POST'])
def route_add_word():
    # Adds a new word with the provided Japanese and English terms
    data = request.json
    japanese = data.get('japanese')
    english = data.get('english')
    add_word(japanese, english)
    return jsonify({'message': 'Word added'})
    # Example URL: POST http://localhost:5000/add_word

@app.route('/words', methods=['GET'])
def route_get_words():
    # Retrieves a list of all words with their IDs, Japanese, and English terms
    words = get_words()
    words_list = [{'id': word.id, 'japanese': word.japanese, 'english': word.english} for word in words]
    return jsonify({'words': words_list})
    # Example URL: GET http://localhost:5000/words

@app.route('/update_word/<int:word_id>', methods=['PUT'])
def route_update_word(word_id):
    # Updates an existing word's Japanese and English terms based on its ID
    data = request.json
    new_japanese = data.get('japanese')
    new_english = data.get('english')
    result = update_word(word_id, new_japanese, new_english)
    return jsonify({'message': 'Word updated' if result else 'Word not found'})
    # Example URL: PUT http://localhost:5000/update_word/<word_id>

@app.route('/delete_word/<int:word_id>', methods=['DELETE'])
def route_delete_word(word_id):
    # Deletes a word based on its ID
    result = delete_word(word_id)
    return jsonify({'message': 'Word deleted' if result else 'Word not found'})
    # Example URL: DELETE http://localhost:5000/delete_word/<word_id>

# CRUD routes for Tag
@app.route('/add_tag', methods=['POST'])
def route_add_tag():
    # Adds a new tag with the provided name
    data = request.json
    name = data.get('name')
    add_tag(name)
    return jsonify({'message': 'Tag added'})
    # Example URL: POST http://localhost:5000/add_tag

@app.route('/tags', methods=['GET'])
def route_get_tags():
    # Retrieves a list of all tags with their IDs and names
    tags = get_tags()
    tags_list = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return jsonify({'tags': tags_list})
    # Example URL: GET http://localhost:5000/tags

@app.route('/update_tag/<int:tag_id>', methods=['PUT'])
def route_update_tag(tag_id):
    # Updates an existing tag's name based on its ID
    data = request.json
    new_name = data.get('name')
    result = update_tag(tag_id, new_name)
    return jsonify({'message': 'Tag updated' if result else 'Tag not found'})
    # Example URL: PUT http://localhost:5000/update_tag/<tag_id>

@app.route('/delete_tag/<int:tag_id>', methods=['DELETE'])
def route_delete_tag(tag_id):
    # Deletes a tag based on its ID
    result = delete_tag(tag_id)
    return jsonify({'message': 'Tag deleted' if result else 'Tag not found'})
    # Example URL: DELETE http://localhost:5000/delete_tag/<tag_id>

@app.cli.command('create_db')
def create_db():
    # Creates all database tables using SQLAlchemy models, only needs to be run once
    db.create_all()
    print("Database tables created.")

if __name__ == '__main__':
    # Starts the Flask app and enables debug mode for easier troubleshooting
    app.run(debug=True)

    # Session and quiz feature planned post System Integration