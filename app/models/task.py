from app import db
from flask import abort, make_response


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_json(self):
        if not self.completed_at:
            is_complete = False

        else:
            is_complete = True

        if self.goal_id:
            return {"id" : self.task_id,
                    "title" : self.title,
                    "description" : self.description,
                    "is_complete" : is_complete,
                    "goal_id": self.goal_id}
        else:
            return {"id" : self.task_id,
                    "title" : self.title,
                    "description" : self.description,
                    "is_complete" : is_complete}
    

    def update_task(self, update_body):

        self.title = update_body["title"]
        self.description = update_body["description"]
        
        if "completed_at" in update_body:
            self.completed_at = update_body["completed_at"]


    @classmethod
    def from_json(cls, request_body):

        if "title" not in request_body or "description" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

        if "completed_at" in request_body:    
            new_task = cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at = request_body["completed_at"])

        elif "completed_at" not in request_body:
            new_task = cls(
            title=request_body["title"],
            description=request_body["description"])
        
        return new_task


