from flask import abort, make_response
from ..models.task import Task

def validate_task(id):
	try:
		id = int(id)
	except:
		return abort(make_response({"message": f"task {id} is invalid"}, 400))

	task = Task.query.get(id)

	if not task:
		abort(make_response({"message": f"task {id} not found"}, 404))

	return task
