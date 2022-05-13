from flask import abort, make_response
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def validate_goal(goal_id):
        '''Validates that goal id is valid and exists'''
        try:
            goal_id = int(goal_id)
        except:
            abort(make_response({"msg": f"Invalid id: {goal_id}"}, 400))

        result = Goal.query.get(goal_id)
        if not result:
            abort(make_response({"msg": f"Could not find goal with id: {goal_id}"}, 404))
        return result

    def goal_response(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
