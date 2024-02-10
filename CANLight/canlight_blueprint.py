from flask import Blueprint, render_template

canlight_blueprint = Blueprint('canlight', __name__, template_folder='CANLight')

@canlight_blueprint.route('/canlight')
def canlight():
    # Placeholder response, you can later update it to render a template
    return render_template('canlight.html')
