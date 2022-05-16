from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)

    def goal_to_json(self):
        json_response = {
            "id": self.goal_id,
            "title": self.title
        }
        if self.tasks:
            json_response["tasks"]= self.title
    
        return json_response

    def update_goal(self, request_body):
        self.title = request_body["title"]
    

    @classmethod
    def create_goal(cls, request_body):
        new_goal = cls(
        title = request_body["title"])
            
        return new_goal


    def add_tasks(self, response_body):
        if response_body["task_ids"]:
            self.tasks = response_body["task_ids"]


    

# goal_id = goal_id,