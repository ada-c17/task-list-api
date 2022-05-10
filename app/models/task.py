from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        return dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = bool(self.completed_at)
        )
    @classmethod
    def from_dict(cls, data_dict):
        # if "is_complete" in data_dict:
        #     return cls(
        #         #id = data_dict["id"],
        #         title = data_dict["title"],
        #         description = data_dict["description"],
        #         is_complete = data_dict["is_complete"]
        #     )
        # else:
        return cls(
                #id = data_dict["id"],
                title = data_dict["title"],
                description = data_dict["description"]
            )

    def replace_details(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]
        #self.completed_at = data_dict["is_complete"]
