from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None) #time_date, need to have option for null or None
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def complete_or_not(self):
        '''
        Converts 'completed_at' task attribute to Boolean for 'is_completed' variable in response body
        '''
        if self.completed_at is not None:
            return True
        else:
            return False
    
    def to_dict(self):
        if self.goal:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.complete_or_not(),
                "goal_id": self.goal_id}
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.complete_or_not()}

    # Example helper function:
    # def to_dict(self):
    #     return {
    #             "id": self.id,
    #             "driver": self.driver.name,
    #             "team": self.driver.team,
    #             "mass_kg": self.mass_kg
    #         }

