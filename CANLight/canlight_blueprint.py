from flask import Blueprint

canlight_blueprint = Blueprint('canlight', __name__, template_folder='templates')

@canlight_blueprint.route('/canlight')
def canlight():
    # Placeholder response, you can later update it to render a template
    return "CANLight page under construction"
