from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship("Goal", back_populates="tasks")
# Old code when we were using a fake database
# Use this to generate unique integer ID for new task instance
# task_id_count = 0

# Create a class of Task instances, where each instance has the following attributes:
#   id: a unique integer ID. This should be set within the class, not given by the client
#   title: a string giving the title of the task
#   description: a string describing the task
#   completed_date: a string that contains a date for when the task was completed
# class Task:

#     def __init__(self, title, description, completed_date):
#         global task_id_count
#         self.id = task_id_count
#         task_id_count += 1
#         self.title = title
#         self.description = description
#         self.completed_date = completed_date