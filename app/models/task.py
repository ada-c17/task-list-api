from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

# class Task:
#     def __init__(self, id, title, description, completed_at=None):
#         self.id = id
#         self.title = title
#         self.description = description
#         self.completed_at = completed_at


# tasks = [
#     Task(1, "Go shopping", "buy everything"),
#     Task(2, "Prepare meal", "lunch for saturday"),
#     Task(3, "Prepare meal", "dinner for Monday"),
#     Task(4, "Laundry", "Kids clothes")
# ]