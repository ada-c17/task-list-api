from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    @classmethod
    def make_goal(cls,request_body):
        new_goal = cls(title = request_body["title"])
            
        return new_goal

    def to_json(self):
        return {"id": self.goal_id, 
                "title": self.title}