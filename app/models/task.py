from app import db
from flask import jsonify, abort, make_response

class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_json(self):
        if not self.completed_at:
            is_complete = False
        else:
            is_complete = True

        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
        }

    @classmethod
    def validate(cls, task_id):
        try:
            task_id = int(task_id)
        except:
            abort(make_response(jsonify(f"{task_id} is not a valid task id."),400))
        task = cls.query.get(task_id)  
        if task:
            return task
        abort(make_response(jsonify(f"Task with id of {task_id} was not found"),404))

    @classmethod
    def create(cls,request_body):
        new_task = cls(
        title = request_body['title'],
        description = request_body['description'],
        completed_at = request_body.get('completed_at', None)
        
    )
        return new_task

    def update(self,request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
