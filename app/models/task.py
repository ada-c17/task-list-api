from app import db
from flask import request, abort, make_response

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_json(self):            
        rsp = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.completed_at is not None
        }

        if self.goal_id: 
            rsp['goal_id'] = self.goal_id

        return rsp
    

    def from_json(user_request):
        if 'title' not in user_request or 'description' not in user_request:
            abort(make_response({'details': 'Invalid data'}, 400))

        return Task(title=user_request['title'], 
                    description=user_request['description'],
                    completed_at = user_request.get('completed_at'))
    

    def from_json_to_update(self, user_request):
        if 'title' in user_request:
            self.title = user_request['title']

        if 'description' in user_request:    
            self.description = user_request['description']

        if 'completed_at' in user_request:
            self.completed_at = user_request['completed_at']

        return self
