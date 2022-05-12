from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def to_dict(self):
        dict = {
            "id": self.goal_id,
            "title": self.title
        }
        
        return dict   