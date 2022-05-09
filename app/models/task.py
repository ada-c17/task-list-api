# from urllib import response
# from pandas import describe_option
# from sqlalchemy import true
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None)


    def to_dictionary(self):
        # if self.completed_at:
        #     completed = True
        # else:
        #     completed = False
        response = {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : True if self.completed_at else False
        }
        return response