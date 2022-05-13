from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return {"goal":{
            "id": self.id, 
            "title": self.title}
        }

    def to_dict_basic(self):
        return {
            "id": self.id, 
            "title": self.title
            }
