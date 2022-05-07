from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None, nullable=True)
    
    def to_json(self):
        complete = None
        if self.completed_at == None:
            complete = False
        else:
            complete = True
       
        return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "is_complete":complete
                }
    # def to_json_with_task(self):
    #     complete = None
    #     if self.completed_at == None:
    #         complete = False
    #     else:
    #         complete = True
       
    #     return {
    #         "task": {
    #             "id": self.id,
    #             "title": self.title,
    #             "description": self.description,
    #             "is_complete": complete 
    #     }
    #     }

    @classmethod
    def create(cls, req_body):
        new_task = cls(
            title = req_body["title"],
            description = req_body["description"],
        )
        return new_task

    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]

    