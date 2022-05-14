from app import db
from flask import jsonify, abort, make_response
# from requests import requests

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goals = db.relationship("Goal")

    def to_json(self):
        is_complete = self.completed_at != None
        
        hash_map = {
            "id" : self.task_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : is_complete
            }
        if self.goal_id:
            hash_map["goal_id"] = self.goal_id

        return hash_map    


    @classmethod
    def create_task(cls, request_body):
        try:
            try:
                new_task = cls(
                title=request_body['title'],
                description=request_body['description'],
                completed_at=request_body['completed_at']
                )
            except KeyError: 
                new_task = cls(
                title=request_body['title'],
                description=request_body['description'],
            )
            return new_task
        except:
            return abort(make_response({"details": "Invalid data"}, 400))
        

    # def to_dict(self):
    #     return {
    #     "task": {
    #         "id": self.id,
    #         "task_id": self.id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": self.completed_at
            



    # @classmethod
    # def from_dict(cls, data_dict):
    #     return cls(
    #         title=data_dict["title"],
    #         description=data_dict["description"],
    #         completed_at=data_dict["completed_at"],
    #     )


        #return dict(
        #     id=self.task_id,
        #     title = self.title,
        #     description=self.description,
        #     is_complete = True if self.completed_at else False
        # )