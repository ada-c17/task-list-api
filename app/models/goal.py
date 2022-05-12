from app import db
from flask import abort, make_response


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def make_goal_dict(self):
        goal_dict = {
                "id": self.goal_id,
                "title": self.title,
        }
    
        return goal_dict

    @classmethod
    def validate_goal(cls, goal_id):
        try:
            goal_id = int(goal_id)
        except:
            abort(make_response({"Message":f"Goal {goal_id} invalid"}, 400))

        goal = Goal.query.get(goal_id)

        if not goal:
            abort(make_response({"Message":f"Goal {goal_id} not found"}, 404))

        return goal
