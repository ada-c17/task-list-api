from app import db
import requests
import os

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime) 
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def to_dict(self):
        status = True if self.completed_at is not None else False
        result = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": status
            }
        if self.goal_id != None:
            result["goal_id"] = self.goal_id
        return result

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]

    def congrats_post(self):
        channel_name = "task-notifications"
        headers = {"Authorization": os.environ.get("SLACK_AUTHORIZATION")}
        text = f"Someone just completed the task {self.title}"
        url = f"https://slack.com/api/chat.postMessage?channel={channel_name}&text={text}&pretty=1"
        requests.post(url, headers=headers)

    @classmethod
    def create(cls, request_body):
        from app.routes.helper_routes import validate_datetime
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=validate_datetime(request_body)
            )
