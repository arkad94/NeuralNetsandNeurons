from gevent import monkey
monkey.patch_all()
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, redirect
from urllib.parse import urlencode, quote_plus
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
from extensions import socketio
from JLOAI.jlo_ai_blueprint import jlo_ai_blueprint
from CANLight.canlight_blueprint import canlight_blueprint

app = Flask(__name__, template_folder='../templates')
app.register_blueprint(jlo_ai_blueprint, url_prefix='/jlo_ai')
app.register_blueprint(canlight_blueprint, url_prefix='/canlight')

# Load environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Initialize Flask and its extensions

app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jlo_ai.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio.init_app(app, async_mode='gevent')




# Setup OAuth
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    userinfo_url = f'https://{os.environ.get("AUTH0_DOMAIN")}/userinfo'
    resp = oauth.auth0.get(userinfo_url)
    userinfo = resp.json()
    session['user'] = userinfo
    return redirect("/")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    if 'user' in session:
        # User is logged in, render the index page with user session details
        return render_template('index.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    else:
        # User is not logged in, render the home page
        return render_template("home.html")


# Clear the Jinja2 cache
app.jinja_env.cache = {}

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler

    # Get port number from the environment variable (Heroku sets it), or set to 5000
    port = int(os.environ.get('PORT', 5000))

    http_server = WSGIServer(('', port), app, handler_class=WebSocketHandler)
    http_server.serve_forever()