from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)


    required_attributes = {
        "title":True,
        "description":True,
        "is_complete":True,
    }
    # Instance methods:

    def self_to_dict(self):
        if self.completed_at is not None:
            is_completed = True
        else:
            is_completed = False
        response = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_completed}
        return response
    
    def update_self(self, data_dict):
        for key in data_dict.keys():
            if hasattr(self, key):
                setattr(self, key, data_dict[key])
            else:
                raise ValueError(key)




