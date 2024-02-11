from flask import Blueprint, request, jsonify, render_template

canlight_blueprint = Blueprint('canlight', __name__, template_folder='CANLight')

# In-memory command storage
current_command = None

@canlight_blueprint.route('/canlight')
def canlight():
    # Render the CANLight page
    return render_template('canlight.html')

@canlight_blueprint.route('/store-command', methods=['POST'])
def store_command():
    global current_command
    current_command = request.json.get('command')
    return jsonify({"status": "success", "message": "Command stored"})

@canlight_blueprint.route('/get-command', methods=['GET'])
def get_command():
    global current_command
    command_to_send = current_command
    current_command = None  # Reset the command after it's retrieved
    return jsonify({"command": command_to_send})
