from datetime import datetime
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    # CHILD - MANY TO ONE
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    # TURN TO JSON
    def t_json(self):
        tast_dict = {
                "id": self.task_id,
                "title": self.title,
                "description" : self.description,
                "is_complete" : True if self.completed_at else False
        }

        if self.goal_id:
            tast_dict["goal_id"] = self.goal_id

        return tast_dict


    # UPDATE
    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]


    # CREATE
    @classmethod
    def create(cls, request_body):
        return cls(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body.get("completed_at", None))

    # MARK
    def patch_complete(self):
        self.completed_at = datetime.now()

    # MARK
    def patch_imcomplete(self):
        self.completed_at = None

