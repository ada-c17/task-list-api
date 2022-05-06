from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #I think types : String with a limited length and Text for description are better suits this model
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable =True)
