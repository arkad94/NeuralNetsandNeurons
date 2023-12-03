from models import db, User, Quiz, UserProgress, UserSettings, Session, Word, Tag

# CRUD for User
def add_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

def get_users():
    return User.query.all()

def update_user(user_id, new_username, new_email):
    user = User.query.get(user_id)
    if user:
        user.username = new_username
        user.email = new_email
        db.session.commit()
        return True
    return False

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

# CRUD for Quiz (Implement similarly as User)

# CRUD for UserProgress (Implement similarly as User)

# CRUD for UserSettings (Implement similarly as User)

# CRUD for Session (Implement similarly as User)

# CRUD for Word
def add_word(japanese, english):
    new_word = Word(japanese=japanese, english=english)
    db.session.add(new_word)
    db.session.commit()

def get_words():
    return Word.query.all()

def update_word(word_id, new_japanese, new_english):
    word = Word.query.get(word_id)
    if word:
        word.japanese = new_japanese
        word.english = new_english
        db.session.commit()
        return True
    return False

def delete_word(word_id):
    word = Word.query.get(word_id)
    if word:
        db.session.delete(word)
        db.session.commit()
        return True
    return False

# CRUD for Tag
def add_tag(name):
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

def get_tags():
    return Tag.query.all()

def update_tag(tag_id, new_name):
    tag = Tag.query.get(tag_id)
    if tag:
        tag.name = new_name
        db.session.commit()
        return True
    return False

def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        return True
    return False
