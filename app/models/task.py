from app import db

'''
"task" = {
    "id": 1,
    "title": "Fold the laundry",
    "description": "Do this on a counter",
    "is_complete": false

}
'''

# creating a Task model with columns in SQLalchemy
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)  # what is nullable
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {
            "task": {
                "id": self.task_id,
                "TITLE": self.title,
                "description": self.description,
                "is_complete": self.completed_at
             }
        }

    # #no task_id here
    # def update(self, request_body):
    #     self.title = request_body["title"]
    #     self.description = request_body["description"]
    #     # self.is_complete = request_body["completed_at"]
    #     self.completed_at = request_body["completed_at"]


    # no task_id here
    # @classmethod
    # def create(cls, request_body):
    #     new_task = cls(
    #         title=request_body["title"],
    #         description=request_body["description"],
    #         # is_complete = request_body["completed_at"]
    #         is_complete = request_body["is_complete"]
    #     )
    #     return new_task