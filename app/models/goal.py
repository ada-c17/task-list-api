from app import db
from flask import jsonify, abort, make_response

class Goal(db.Model):

    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_json(self):

        return {
                "id": self.goal_id,
                "title": self.title
        }

    @classmethod
    def validate(cls, goal_id):
        try:
            goal_id = int(goal_id)
        except:
            abort(make_response(jsonify(f"{goal_id} is not a valid goal id."),400))
        goal = cls.query.get(goal_id)  
        if goal:
            return goal
        abort(make_response(jsonify(f"Goal with id of {goal_id} was not found"),404))

    @classmethod
    def create(cls,request_body):
        new_goal = cls(
        title = request_body['title']
        
    )
        return new_goal

    def update(self,request_body):
        self.title = request_body["title"]
