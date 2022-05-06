from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None)
    is_completed = db.Column(db.Boolean, default=False)

    def make_dict(self):
        data_dict= dict(
                id=self.task_id,
                title=self.title,
                description=self.description,  
            )
        if self.is_completed == False: 
            data_dict["is_completed"] = self.is_completed
        else: 
            data_dict["completed_at"] = self.completed_at
        return data_dict
    
    def replace_all_details(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"], 
            description = data_dict["description"],
            )