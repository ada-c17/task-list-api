from app import db
from flask import jsonify, abort, make_response

class Goal(db.Model):

    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)