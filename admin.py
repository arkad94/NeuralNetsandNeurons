# Importing necessary classes and functions from 'models.py'. These are used to interact with the database.
from models import db, User, Quiz, UserProgress, UserSettings, Session, Word, Tag, ChangeLog
# Importing 'func' from SQLAlchemy for SQL functions like aggregations.
from sqlalchemy.sql import func
# Importing BackgroundScheduler for running background tasks.
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize a background scheduler for running scheduled tasks.
scheduler = BackgroundScheduler()

# CRUD Operations for User
# CRUD: Create, Read, Update, Delete - essential database operations.

def add_user(username, email):
    # Create a new User instance with provided username and email.
    new_user = User(username=username, email=email)
    # Add this new user to the database session, staging it for commit.
    db.session.add(new_user)
    # Commit the staged changes to the database, saving the new user.
    db.session.commit()

def get_users():
    # Fetch and return all user records from the database.
    return User.query.all()

def update_user(user_id, new_username, new_email):
    # Retrieve a user by ID from the database.
    user = User.query.get(user_id)
    # If user exists, update the username and email.
    if user:
        user.username = new_username
        user.email = new_email
        db.session.commit()  # Commit changes to the database.
        return True  # Indicate successful update.
    return False  # Indicate that the user does not exist.

def delete_user(user_id):
    # Retrieve a user by ID from the database.
    user = User.query.get(user_id)
    # If user exists, delete it from the database.
    if user:
        db.session.delete(user)
        db.session.commit()  # Commit changes to the database.
        return True  # Indicate successful deletion.
    return False  # Indicate that the user does not exist.

# CRUD Operations for Quiz, UserProgress, UserSettings, Session
# Implement CRUD operations for these models similar to the User model.

# CRUD Operations for Word
def add_word(japanese, english):
    # Create a new Word instance with Japanese and English translations.
    new_word = Word(japanese=japanese, english=english)
    db.session.add(new_word)  # Add to database session.
    db.session.commit()  # Save the new word to the database.
    # Logging the addition of a new word.
    add_change_log('Word', new_word.id, 'insert', f'Added word: {japanese} - {english}')

def get_words():
    # Fetch and return all word records from the database.
    return Word.query.all()

def update_word(word_id, new_japanese, new_english):
    # Retrieve a word by ID from the database.
    word = Word.query.get(word_id)
    # If word exists, update its Japanese and English translations.
    if word:
        word.japanese = new_japanese
        word.english = new_english
        db.session.commit()  # Commit changes to the database.
        # Logging the update of a word.
        add_change_log('Word', word.id, 'update', f'Updated word to {new_japanese} - {new_english}')
        return True  # Indicate successful update.
    return False  # Indicate that the word does not exist.

def delete_word(word_id):
    # Retrieve a word by ID from the database.
    word = Word.query.get(word_id)
    # If word exists, delete it from the database.
    if word:
        db.session.delete(word)
        db.session.commit()  # Commit changes to the database.
        # Logging the deletion of a word.
        add_change_log('Word', word.id, 'delete', f'Deleted word: {word.japanese} - {word.english}')
        return True  # Indicate successful deletion.
    return False  # Indicate that the word does not exist.

# CRUD Operations for Tag
def add_tag(name):
    # Create a new Tag instance with a given name.
    new_tag = Tag(name=name)
    db.session.add(new_tag)  # Add to database session.
    db.session.commit()  # Save the new tag to the database.
    # Logging the addition of a new tag.
    add_change_log('Tag', new_tag.id, 'insert', f'Added tag: {name}')

def get_tags():
    # Fetch and return all tag records from the database.
    return Tag.query.all()

def update_tag(tag_id, new_name):
    # Retrieve a tag by ID from the database.
    tag = Tag.query.get(tag_id)
    # If tag exists, update its name.
    if tag:
        tag.name = new_name
        db.session.commit()  # Commit changes to the database.
        # Logging the update of a tag.
        add_change_log('Tag', tag.id, 'update', f'Updated tag to {new_name}')
        return True  # Indicate successful update.
    return False  # Indicate that the tag does not exist.

def delete_tag(tag_id):
    # Retrieve a tag by ID from the database.
    tag = Tag.query.get(tag_id)
    # If tag exists, delete it from the database.
    if tag:
        db.session.delete(tag)  # Delete the tag from the session.
        db.session.commit()  # Commit the transaction to the database.
        # Logging the deletion of a tag.
        add_change_log('Tag', tag.id, 'delete', f'Deleted tag: {tag.name}')
        return True  # Indicate successful deletion.
    return False  # Indicate that the tag does not exist.

# CRUD Operations for ChangeLog
def add_change_log(table_name, record_id, action, details=None):
    # Create a new log entry for changes made in the database.
    new_log = ChangeLog(table_name=table_name, record_id=record_id, action=action, details=details)
    db.session.add(new_log)  # Add log entry to the database session.
    db.session.commit()  # Save the log entry to the database.

# Update existing CRUD functions to include logging.
# Example for add_user (similar updates should be applied to other CRUD functions).
def add_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    # Log the addition of a new user.
    add_change_log('User', new_user.id, 'insert', f'Added user {username}')

# Define the function to generate a report from the ChangeLog.
def generate_report():
    # Fetch all log entries, ordered by timestamp in descending order.
    logs = ChangeLog.query.order_by(ChangeLog.timestamp.desc()).all()
    report = []
    # Compile a report based on the log entries.
    for log in logs:
        report.append(f"{log.timestamp}: {log.action} on {log.table_name} (ID: {log.record_id}) - {log.details}")
    return "\n".join(report)  # Return the compiled report as a string.

# Initialize the background scheduler.
scheduler = BackgroundScheduler()

# Define a job to automatically generate a report.
def scheduled_report_job():
    report = generate_report()
    # Additional code to handle the generated report (e.g., saving, emailing, etc.)

# Add the report generation job to the scheduler with a 24-hour interval.
scheduler.add_job(scheduled_report_job, 'interval', hours=24)  # Interval can be adjusted as needed.

# Start the scheduler to begin running scheduled jobs.
scheduler.start()

# (Include any remaining parts of the existing script, such as initialization and main routine)


