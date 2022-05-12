from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goals")

    def to_dict(self):
        return {
            "id":self.goal_id,
            "title":self.title,
        }

    def to_dict_advanced(self):
        '''
        Includes advanced tasks information
        '''
        return {
            "id":self.goal_id,
            "title":self.title,
            "tasks":[task.to_dict_goals() for task in self.tasks]
        }
