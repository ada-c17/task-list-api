from app import db
from flask import make_response, abort 
# from app.routes.helpers import validate_task

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates = "goal", lazy = True)

    def to_json(self):
        
        return {"id" : self.goal_id,
                "title" : self.title}
    

    def update_goal(self, update_body):
            self.title = update_body["title"]

    # def link_goals_to_task(self, request_body):
    #     task_list = []
    #     for task_id in request_body["task_ids"]:
    #         task = validate_task(task_id)
    #         task_list.append(task)

    #     for task in task_list: 
    #         if task not in self.tasks:
    #             self.tasks.append(task)

    @classmethod
    def from_json(cls, request_body):

        if "title" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

        new_goal = cls(
            title=request_body["title"])

        return new_goal


