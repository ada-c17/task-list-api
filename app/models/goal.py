from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)

    def to_dict(self):
        return dict(
            id = self.goal_id,
            title = self.title,
            )

    def one_goal_to_dict(self):
        result = {}
        result["goal"] = self.to_dict()
        return result

    def replace_details(self, data_dict):
        self.title = data_dict["title"]
