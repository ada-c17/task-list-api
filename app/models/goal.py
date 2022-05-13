from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy = True)
    # I checked how to use laze in this website...
    #https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef
    
    
    def to_dict_goal(self):
        response = {"id": self.goal_id,
            "title": self.title}
        return response
    
    