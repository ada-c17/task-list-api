from app import db
from app.error_responses import MissingValueError

class Goal(db.Model):
    '''A SQLAlchemy.Model subclass representing goal entries in the database.
    
    Goals can optionally be associated with a collection of Task instances
    and used to organize related sets of tasks.

    Attributes:
        goal_id: int
        title: str
        tasks: list[Task]
    '''

    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', back_populates='goal')

    @classmethod
    def create(cls, goal_details: dict):
        '''Creates and returns a new Goal instance from input dict.'''

        if 'title' not in goal_details:
            raise MissingValueError
        return cls(title = goal_details['title'])
    
    def update(self, new_details: dict):
        '''Updates the attributes of an existing Goal instance.'''

        for k,v in new_details.items():
            if k in self.__dict__:
                setattr(self, k, v)


class TasksGoal():
    '''Wraps a Goal instance in order to modify JSONification.'''

    def __init__(self, goal: Goal):
        self._ = goal
