from flask import Flask, jsonify, request
from models import db
from admin import (add_user, get_users, update_user, delete_user, 
                   add_word, get_words, update_word, delete_word,
                   add_tag, get_tags, update_tag, delete_tag)

# Set up a new Flask application.
app = Flask(__name__)
# Configure the application to use an SQLite database named jlo_ai.db.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jlo_ai.db'
# Initialize the database, making it ready for use with our app.
db.init_app(app)

# Define the root ('/') route. This is the default page for our web app.
@app.route('/')
def index():
    # This function simply returns a string to let us know the app is working.
    return 'Flask is Working!'

# User CRUD (Create, Read, Update, Delete) routes:

# Add a new user. The URL example shows how to test this route.
@app.route('/add_user/<username>/<email>', methods=['POST'])
def route_add_user(username, email):
    add_user(username, email)  # Call the add_user function from admin.py.
    return jsonify({'message': 'User added'})
    # Example URL: POST http://localhost:5000/add_user/john/doe@example.com

# Get a list of all users. The URL example shows how to access this data.
@app.route('/users', methods=['GET'])
def route_get_users():
    users = get_users()  # Get all users from the database.
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify({'users': users_list})
    # Example URL: GET http://localhost:5000/users

# Update a user's information. The URL example shows how to test this route.
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def route_update_user(user_id):
    data = request.json  # Extract data from the request.
    username = data.get('username')
    email = data.get('email')
    result = update_user(user_id, username, email)  # Update the user.
    return jsonify({'message': 'User updated' if result else 'User not found'})
    # Example URL: PUT http://localhost:5000/update_user/1

# Delete a user. The URL example shows how to test this route.
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def route_delete_user(user_id):
    result = delete_user(user_id)  # Delete the user from the database.
    return jsonify({'message': 'User deleted' if result else 'User not found'})
    # Example URL: DELETE http://localhost:5000/delete_user/1

# Word CRUD routes:

# Add a new word. The URL example shows how to test this route.
@app.route('/add_word', methods=['POST'])
def route_add_word():
    data = request.json  # Extract data from the request.
    japanese = data.get('japanese')
    english = data.get('english')
    add_word(japanese, english)  # Add the new word to the database.
    return jsonify({'message': 'Word added'})
    # Example URL: POST http://localhost:5000/add_word

# Get a list of all words. The URL example shows how to access this data.
@app.route('/words', methods=['GET'])
def route_get_words():
    words = get_words()  # Get all words from the database.
    words_list = [{'id': word.id, 'japanese': word.japanese, 'english': word.english} for word in words]
    return jsonify({'words': words_list})
    # Example URL: GET http://localhost:5000/words

# Update a word's information. The URL example shows how to test this route.
@app.route('/update_word/<int:word_id>', methods=['PUT'])
def route_update_word(word_id):
    data = request.json  # Extract data from the request.
    new_japanese = data.get('japanese')
    new_english = data.get('english')
    result = update_word(word_id, new_japanese, new_english)  # Update the word.
    return jsonify({'message': 'Word updated' if result else 'Word not found'})
    # Example URL: PUT http://localhost:5000/update_word/1

# Delete a word. The URL example shows how to test this route.
@app.route('/delete_word/<int:word_id>', methods=['DELETE'])
def route_delete_word(word_id):
    result = delete_word(word_id)  # Delete the word from the database.
    return jsonify({'message': 'Word deleted' if result else 'Word not found'})
    # Example URL: DELETE http://localhost:5000/delete_word

# Tag CRUD routes:

# Add a new tag. The URL example shows how to test this route.
@app.route('/add_tag', methods=['POST'])
def route_add_tag():
    data = request.json  # Extract data from the request.
    name = data.get('name')
    add_tag(name)  # Add the new tag to the database.
    return jsonify({'message': 'Tag added'})
    # Example URL: POST http://localhost:5000/add_tag

# Get a list of all tags. The URL example shows how to access this data.
@app.route('/tags', methods=['GET'])
def route_get_tags():
    tags = get_tags()  # Get all tags from the database.
    tags_list = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return jsonify({'tags': tags_list})
    # Example URL: GET http://localhost:5000/tags

# Update a tag's name. The URL example shows how to test this route.
@app.route('/update_tag/<int:tag_id>', methods=['PUT'])
def route_update_tag(tag_id):
    data = request.json  # Extract data from the request.
    new_name = data.get('name')
    result = update_tag(tag_id, new_name)  # Update the tag's name.
    return jsonify({'message': 'Tag updated' if result else 'Tag not found'})
    # Example URL: PUT http://localhost:5000/update_tag/1

# Delete a tag. The URL example shows how to test this route.
@app.route('/delete_tag/<int:tag_id>', methods=['DELETE'])
def route_delete_tag(tag_id):
    result = delete_tag(tag_id)  # Delete the tag from the database.
    return jsonify({'message': 'Tag deleted' if result else 'Tag not found'})
    # Example URL: DELETE http://localhost:5000/delete_tag/1

@app.cli.command('create_db')
def create_db():
    # Command to create all database tables. Only needs to be run once.
    db.create_all()
    print("Database tables created.")

 # Start the Flask application.
# At the end of app.py, after defining routes and before running the app
if __name__ == '__main__':
   
    from admin import scheduler  # Make sure to import the scheduler from admin.py
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
        # Generate initial report
    initial_report = generate_report()
    
    
    app.run(debug=True)
    # Debug mode is enabled for development purposes.
