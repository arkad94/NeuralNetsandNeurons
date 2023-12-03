# Import the database instance and all the models from models.py.
# These models represent the tables in our database.
from models import db, User, Quiz, UserProgress, UserSettings, Session, Word, Tag, ChangeLog
from sqlalchemy.sql import func
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# CRUD operations for User
# CRUD stands for Create, Read, Update, Delete - common operations for managing data.

def add_user(username, email):
    # Create a new User object with a username and email.
    new_user = User(username=username, email=email)
    # Add the new User object to the database session - think of this as preparing the data.
    db.session.add(new_user)
    # Save (commit) the changes to the database, making the addition of the new user permanent.
    db.session.commit()

def get_users():
    # Query the database for all User records.
    # The .all() method fetches all records from the User table.
    return User.query.all()

def update_user(user_id, new_username, new_email):
    # Retrieve a User object from the database by its ID.
    user = User.query.get(user_id)
    # If the user exists, update the username and email with the new values.
    if user:
        user.username = new_username
        user.email = new_email
        # Save the changes to the database.
        db.session.commit()
        return True  # Return True to indicate the operation was successful.
    return False  # If the user does not exist, return False.

def delete_user(user_id):
    # Retrieve a User object from the database by its ID.
    user = User.query.get(user_id)
    # If the user exists, remove it from the database.
    if user:
        db.session.delete(user)
        # Save the changes to the database.
        db.session.commit()
        return True  # Return True to indicate the user was deleted.
    return False  # If the user does not exist, return False.

# CRUD for Quiz
# The operations for Quiz should be implemented similarly to the User CRUD operations above.

# CRUD for UserProgress
# Implement CRUD operations for UserProgress similar to User.

# CRUD for UserSettings
# Implement CRUD operations for UserSettings similar to User.

# CRUD for Session
# Implement CRUD operations for Session similar to User.

# CRUD operations for Word
#Generate Report Function
def generate_report():
    logs = ChangeLog.query.order_by(ChangeLog.timestamp.desc()).all()
    report = []
    for log in logs:
        report.append(f"{log.timestamp}: {log.action} on {log.table_name} (ID: {log.record_id}) - {log.details}")
    return "\n".join(report)


def add_word(japanese, english):
    # Create a new Word object with Japanese and English meanings.
    new_word = Word(japanese=japanese, english=english)
    # Add the new Word object to the database session.
    db.session.add(new_word)
    # Save the new word to the database.
    db.session.commit()
    add_change_log('Word', new_word.id, 'insert', f'Added word: {japanese} - {english}')

def get_words():
    # Query the database for all Word records.
    return Word.query.all()

def update_word(word_id, new_japanese, new_english):
    # Retrieve a Word object by its ID.
    word = Word.query.get(word_id)
    # If the word exists, update its Japanese and English meanings.
    if word:
        word.japanese = new_japanese
        word.english = new_english
        # Save the changes to the database.
        db.session.commit()
        add_change_log('Word', word.id, 'update', f'Updated word from {original_japanese} - {original_english} to {new_japanese} - {new_english}')
    return True  # Return True to indicate the operation was successful.
    return False  # If the word does not exist, return False.

def delete_word(word_id):
    # Retrieve a Word object by its ID.
    word = Word.query.get(word_id)
    # If the word exists, remove it from the database.
    if word:
        db.session.delete(word)
        # Save the changes to the database.
        db.session.commit()
        add_change_log('Word', word.id, 'delete', f'Deleted word: {word.japanese} - {word.english}')               
        return True  # Return True to indicate the word was deleted.
    return False  # If the word does not exist, return False.

# CRUD operations for Tag

def add_tag(name):
    # Create a new Tag object with a name.
    new_tag = Tag(name=name)
    # Add the new Tag object to the database session.
    db.session.add(new_tag)
    # Save the new tag to the database.
    db.session.commit()
    add_change_log('Tag', new_tag.id, 'insert', f'Added tag: {name}')

def get_tags():
    # Query the database for all Tag records.
    return Tag.query.all()

def update_tag(tag_id, new_name):
    # Retrieve a Tag object by its ID.
    tag = Tag.query.get(tag_id)
    # If the tag exists, update its name.
    if tag:
        tag.name = new_name
        # Save the changes to the database.
        db.session.commit()
        add_change_log('Tag', tag.id, 'update', f'Updated tag from {original_name} to {new_name}')
        return True  # Return True to indicate the operation was successful.
    return False  # If the tag does not exist, return False.

def delete_tag(tag_id):
    # Retrieve a Tag object by its ID.
    tag = Tag.query.get(tag_id)
    # If the tag exists, remove it from the database.
    if tag:
        db.session.delete(tag)  # Delete the tag from the session.
        db.session.commit()     # Commit the transaction to make the change permanent in the database.
        add_change_log('Tag', tag.id, 'delete', f'Deleted tag: {tag.name}')
        return True             # Return True to indicate successful deletion.
    return False  # If the tag does not exist, return False.

# CRUD operations for ChangeLog
def add_change_log(table_name, record_id, action, details=None):
    new_log = ChangeLog(table_name=table_name, record_id=record_id, action=action, details=details)
    db.session.add(new_log)
    db.session.commit()

# Update existing CRUD functions to include logging
# Example for add_user (apply similar updates to other CRUD functions)
def add_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    add_change_log('User', new_user.id, 'insert', f'Added user {username}')

# Define the report generation function
def generate_report():
    logs = ChangeLog.query.order_by(ChangeLog.timestamp.desc()).all()
    report = []
    for log in logs:
        report.append(f"{log.timestamp}: {log.action} on {log.table_name} (ID: {log.record_id}) - {log.details}")
    return "\n".join(report)

# Initialize scheduler
scheduler = BackgroundScheduler()

# Define a job to generate a report
def scheduled_report_job():
    report = generate_report()
    # Here you can save the report to a file, send it via email, or store it in the database

# Add the job to the scheduler
scheduler.add_job(scheduled_report_job, 'interval', hours=24)  # Adjust the interval as needed

# Start the scheduler
scheduler.start()

# (Include any remaining parts of the existing script, such as initialization and main routine)

