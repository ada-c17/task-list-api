from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)

    def goal_to_json(self):
        json_response = {
            "id": self.goal_id,
            "title": self.title
        }
        return json_response

    def update_goal(self, request_body):
        self.title = request_body["title"]

    @classmethod
    def create_goal(cls, request_body):
        new_goal = cls(title = request_body["title"])
            
        return new_goal
