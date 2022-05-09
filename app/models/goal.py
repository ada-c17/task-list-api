from app import db
from flask import request,abort, make_response


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates = "goal", lazy = True)

    def goal_to_JSON(self):
        rsp = {
            "goal": {
                "id": self.goal_id,
                "title": self.title,
            }
        }
        if self.tasks:
            rsp["goal"]["tasks"] = self.tasks
        return rsp
    
    @staticmethod
    def check_goal_JSON_request_body():
        request_body = request.get_JSON()
        
        if"title" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

        return request_body
