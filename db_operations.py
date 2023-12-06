# db_operations.py
from models import db, User, Word, Tag, ChangeLog, Report
from sqlalchemy.exc import SQLAlchemyError

# User CRUD Operations
def add_user(username, email):
    try:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        add_change_log('User', new_user.id, 'insert', f'Added user {username}')
        return "User added successfully"
    except SQLAlchemyError as e:
        return f"Error adding user: {e}"

def get_users():
    try:
        return User.query.all()
    except SQLAlchemyError as e:
        return f"Error fetching users: {e}"

def update_user(user_id, new_username, new_email):
    try:
        user = User.query.get(user_id)
        if user:
            user.username = new_username
            user.email = new_email
            db.session.commit()
            add_change_log('User', user.id, 'update', f'Updated user {new_username}')
            return True
        return False
    except SQLAlchemyError as e:
        return f"Error updating user: {e}"

def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            add_change_log('User', user.id, 'delete', f'Deleted user')
            return True
        return False
    except SQLAlchemyError as e:
        return f"Error deleting user: {e}"

# Word CRUD Operations
# Implement similar functions for add_word, get_words, update_word, delete_word

# Tag CRUD Operations
# Implement similar functions for add_tag, get_tags, update_tag, delete_tag

def add_change_log(table_name, record_id, action, details=None):
    try:
        new_log = ChangeLog(table_name=table_name, record_id=record_id, action=action, details=details)
        db.session.add(new_log)
        db.session.commit()
    except SQLAlchemyError as e:
        return f"Error adding change log: {e}"

def generate_report():
    try:
        logs = ChangeLog.query.order_by(ChangeLog.timestamp.desc()).all()
        report_content = "\n".join([f"{log.timestamp}: {log.action} on {log.table_name} (ID: {log.record_id}) - {log.details}" for log in logs])
        new_report = Report(content=report_content)
        db.session.add(new_report)
        db.session.commit()
        return new_report.id
    except SQLAlchemyError as e:
        return f"Error generating report: {e}"

# Continue to define other necessary functions (like reset_database_data)
