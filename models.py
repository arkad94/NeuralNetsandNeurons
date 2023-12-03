from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()

# Association table for many-to-many relationship between Words and Tags
word_tags = Table('word_tags', db.Model.metadata,
    Column('word_id', Integer, ForeignKey('word.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    # Add more fields as needed for password, etc.

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    # Other quiz attributes like description, difficulty

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    word_id = db.Column(db.Integer, ForeignKey('word.id'))
    progress = db.Column(db.String(50))  # Example: 'learning', 'mastered'
    user = relationship("User", backref="progresses")
    word = relationship("Word", backref="progresses")

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    setting = db.Column(db.String(100))  # Example settings
    value = db.Column(db.String(100))    # Value for the setting
    user = relationship("User", backref="settings")

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    session_data = db.Column(db.String(500))  # Store session data
    user = relationship("User", backref="sessions")

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    japanese = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100))
    tags = relationship('Tag', secondary=word_tags, backref='words')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

