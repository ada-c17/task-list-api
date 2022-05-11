from app import db
from flask import make_response, abort

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True) # go to task model and add goal
    # lazy - not going to make instance until you try to use .tasks

    def validate_goal(goal_id):
        try:
            goal_id = int(goal_id)
        except ValueError:
            return abort(make_response({"message":f"Goal {goal_id} invalid"}, 400))

        goal = Goal.query.get(goal_id)

        if goal is None:
            abort(make_response({"message":f"Goal {goal_id} not found"}, 404))

        return goal 

    def to_json(self):
        # json = {
        #     "id": self.goal_id,
        #     "title": self.title
        # }

        # if self.tasks:
        #     json["tasks"] = [task.to_json() for task in self.tasks]

        # return json
            
        return {
            "id": self.goal_id,
            "title": self.title
        }