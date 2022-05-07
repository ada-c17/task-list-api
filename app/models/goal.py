from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            'id': self.goal_id,
            'title': self.title
        }
    
    @classmethod
    def validate_id(cls, target_id):
        try:
            target_id = int(target_id)
        except:
            abort(make_response(jsonify(f"{target_id} is not a valid id."),400))
        
        goal = cls.query.get(target_id)

        if not goal:
            abort(make_response(jsonify(f"A goal with id of {target_id} was not found."),404))
        
        return goal
