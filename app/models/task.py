from app import db
from datetime import datetime

class Task(db.Model):
    ## class variables
    expected_elements = {"title":str, "description":str}
    db_name = "Task"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id")) #note: need to make nullable? or that way by default?
    goal = db.relationship("Goal", back_populates="tasks") #lazy=select/True is default

    def make_response_dict(self):
        if self.completed_at:
            completed = True
        else:
            completed = False
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": completed
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict 

    def create_from_request(self, request_body):
        self.title = request_body["title"],
        self.description = request_body["description"]
        completed = request_body.get("completed_at")
        if completed:
            if type(completed) == str:
                try:
                    #datetime.utcnow() default string
                    is_formatted = datetime.strptime(completed, 
                                                    "%a, %d %B %Y %H:%M:%S %Z")
                except ValueError:
                    try:
                        #yyyy-mm-dd hh:mm:ss format
                        is_formatted = datetime.strptime(completed, 
                                                        "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            #yyyy-mm-dd hh:mm format (omit seconds)
                            is_formatted = datetime.strptime(completed, 
                                                            "%Y-%m-%d %H:%M")
                        except ValueError:
                            is_formatted = False
                if is_formatted:
                    self.completed_at = completed
                    #does not add invalid timestamps to database entry
        return self