from app import db

class Goal(db.Model):
    #class variables
    expected_elements = {"title":str}
    db_name = "Goal"

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal") #lazy=select/True is default

    def make_response_dict(self):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        return goal_dict

    def create_from_request(self, request_body):
        self.title = request_body["title"]
        return self