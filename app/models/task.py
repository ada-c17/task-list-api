from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))


    def to_dict(self):
        if self.goal_id:
            return dict(
            id = self.id,
            goal_id = self.goal_id,
            title = self.title,
            description = self.description,
            is_complete = bool(self.completed_at)
        )
        else:
            return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_complete = bool(self.completed_at)
        )
    @classmethod
    def from_dict(cls, data_dict):
        completed_time = data_dict["completed_at"] if "completed_at" in data_dict else None
        return cls(
                title = data_dict["title"],
                description = data_dict["description"],
                completed_at = completed_time
            )
        # else: 
        # return cls(
        #         title = data_dict["title"],
        #         description = data_dict["description"]
        #     )

    def replace_details(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]
        #self.completed_at = data_dict["is_complete"]
