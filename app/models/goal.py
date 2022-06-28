from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def self_to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,}
    
    def update_self(self, data_dict):
        for key in data_dict.keys():
            if hasattr(self, key):
                setattr(self, key, data_dict[key])
            else:
                raise ValueError(key)


