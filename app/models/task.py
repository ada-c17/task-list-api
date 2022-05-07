from app import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    is_complete = False
    completed_at = None

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete)
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"]
            )
    
    def replace_details(self, data_dict):
        self.title=data_dict["title"]
        self.description=data_dict["description"]
        return self.to_dict()

    def mark_done(self):
        self.is_complete = True
        self.completed_at = db.func.current_timestamp()
        return self.completed_at
