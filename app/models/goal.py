from __future__ import annotations
from flask import abort
from app import db
from app.error_responses import MissingValueError, make_error_response

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
    display_full = False

    @classmethod
    def create(cls, goal_details: dict) -> Goal:
        '''Creates and returns a new Goal instance from input dict.'''

        if 'title' not in goal_details:
            abort(make_error_response(MissingValueError()))
        return cls(title = goal_details['title'])
    
    def update(self, new_details: dict) -> None:
        '''Updates the attributes of an existing Goal instance.'''

        try:
            self.title = new_details['title']
        except KeyError:
            abort(make_error_response(MissingValueError()))
