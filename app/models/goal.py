from app import db

"""Answer the following questions. 
These questions will help you become familiar with the API, 
and make working with it easier.

What is the responsibility of this endpoint?
What is the URL and HTTP method for this endpoint?
What are the two required arguments for this endpoint?
How does this endpoint relate to the Slackbot API key (token) we just created?"""

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Goal", back_populates="goal")

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title
            )

    def update(self,request_body):
        self.title = request_body["title"]
    
    @classmethod
    def create(cls, request_body):
        return cls(
            title=request_body["title"]
            )



