from flask import Blueprint, jsonify
from datetime import datetime

date_bp = Blueprint("date_bp", __name__)

@date_bp.route("/api/date")
def get_date():
    now = datetime.now()

    return jsonify({
        "day": now.strftime("%A"),
        "date": now.strftime("%B %d"),
        "time": now.strftime("%I:%M %p")
    })