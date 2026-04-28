from flask import Blueprint, jsonify, request
from SMTplugins.FakeLight.fakeLight_widget import FakeLightWidget

fakeLight_bp = Blueprint('fakeLight', __name__)

light_instance = FakeLightWidget()

@fakeLight_bp.route('/api/light/status', methods=['GET'])
def get_light_status():
    return jsonify({"state": light_instance.update()})

@fakeLight_bp.route('/api/light/toggle', methods=['POST'])
def toggle_light():
    new_state = light_instance.toggle()
    return jsonify({"state": new_state})