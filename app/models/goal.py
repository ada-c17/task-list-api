from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def make_dict(self): 
        data_dict=dict(
                id=self.goal_id,
                title=self.title,
            )

        return data_dict

    def replace_title(self, data_dict):
        self.title = data_dict["title"]

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"])