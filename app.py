from flask import Flask
from models import db

app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jlo_ai.db'

# Initialize the db with the Flask app
db.init_app(app)

@app.route('/')
def index():
    return 'Flask is Working!'

@app.cli.command('create_db')
def create_db():
    db.create_all()
    print("Database tables created.")

if __name__ == '__main__':
    app.run(debug=True)
