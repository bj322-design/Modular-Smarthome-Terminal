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
    data = request.get_json()
    task_id = data.get('task_id')
    
    if not task_id:
        return jsonify({"error": "No task ID provided"}), 400

    try:
        service = tasks.get_service()
        if not service:
            return jsonify({"error": "Authentication failed"}), 401

        # Use patch to update the status to 'completed'
        # Google requires the task ID and the '@default' list ID
        service.tasks().patch(
            tasklist='@default', 
            task=task_id, 
            body={'status': 'completed'}
        ).execute()
        
        return jsonify({"status": "success", "message": "Task marked as completed"})

    except Exception as e:
        print(f"Error completing task: {e}")
        return jsonify({"error": "Failed to update task on Google server", "details": str(e)}), 500