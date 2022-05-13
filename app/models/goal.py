from app import db

class Goal(db.Model):
    '''
        A goal that is set. May or may not have associated tasks.

        Expected elements on creation:
            title (str): name of goal
    '''
    #class variables
    expected_elements = {"title":str}
    db_name = "Goal"

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal") #lazy=select/True is default

    def make_response_dict(self):
        '''Build and return dict of Goal instance attributes'''
        goal_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        return goal_dict

    def create_from_request(self, request_body):
        '''Create new Goal from request body, return created Goal instance'''
        self.title = request_body["title"]
        return self