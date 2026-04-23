from flask import Blueprint, jsonify, request
from SMTplugins.GoogleTasks.googleTasks_widget import GoogleTasksWidget

googleTasks_bp = Blueprint('googleTasks_bp', __name__)
tasks = GoogleTasksWidget()

@googleTasks_bp.route("/api/google/tasks")
def get_google_tasks():
    data = tasks.update()
    # Ensure data is always a list, even if empty
    if data is None:
        return jsonify([])
    return jsonify(data)

@googleTasks_bp.route('/api/google/tasks/complete', methods=['POST'])
def complete_task():
    task_id = request.json.get('task_id')
    if not task_id:
        return jsonify({"error": "No task ID provided"}), 400

    # Logic to mark task as completed in Google
    service = tasks.get_service() # Helper method to get the 'build' object
    service.tasks().patch(tasklist='@default', task=task_id, body={'status': 'completed'}).execute()
    
    return jsonify({"status": "success"})