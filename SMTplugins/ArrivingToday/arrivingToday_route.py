from flask import Blueprint, jsonify
from SMTplugins.ArrivingToday.arrivingToday_widget import ArrivingTodayWidget

arriving_today_bp = Blueprint('arriving_today', __name__)
widget_instance = ArrivingTodayWidget()

@arriving_today_bp.route('/api/arriving-today/<client_id>')
def get_arriving_today_data(client_id):
    data = widget_instance.widgetData(client_id)
    return jsonify(data)