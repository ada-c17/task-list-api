from flask import Blueprint

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    pass

@tasks_bp.route("", methods=["POST"])
def create_new_task(request):
    pass

@tasks_bp.route("/<id>", methods=["GET"])
def get_task_by_id():
    pass

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task_by_id(request):
    pass

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task_by_id():
    pass