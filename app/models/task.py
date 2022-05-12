from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable = True)

    @classmethod
    def make_task(cls,request_body):
        if "completed_at" in request_body:
            new_task = cls(title = request_body["title"], 
                        description = request_body["description"], 
                        completed_at = request_body["completed_at"])
        elif "completed_at" not in request_body:
            new_task = cls(title = request_body["title"], 
                        description = request_body["description"])
            
        return new_task

    def to_json(self):
        is_complete = False if not self.completed_at else True

        json_response = {"id": self.task_id, 
                "title": self.title, 
                "description": self.description, 
                "is_complete": is_complete}
        
        if self.goal_id:
            json_response["goal_id"] = self.goal_id
        
        return json_response
    
    def update_task(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        if "completed_at" in request_body:
            self.completed_at = request_body["completed_at"]
