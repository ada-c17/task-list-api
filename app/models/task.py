from app import db

#child class
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) #index=True, unique=True with or without don't work for unique value
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")
    
    #depends on None(code)/null(db)
    def completed(self):
        if not self.completed_at:
            return False
        else:
            return True
    
    #display jsonify dict
    def to_json(self):
        satus = self.completed()
        return {
            #"task": {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": satus
            #}
        }