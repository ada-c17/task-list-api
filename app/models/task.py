from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=None)


    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete,
            

        )

    def to_dict_one_task(self):
        return {
            "task": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete,
                # "completed_at": self.completed_at
                # "is_complete": False
            }
        }
  
 
        

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            # is_complete=data_dict["is_complete"],
            # completed_at=data_dict["completed_at"]
            # is_complete=data_dict["is_complete"],
            
        )

    def replace_details(self, data_dict):
        self.title=data_dict["title"]
        self.description=data_dict["description"]
        # self.is_complete=data_dict["is_complete"]
        
        return self.to_dict()



    # completed_at : default null (none)

    # is_complete(db.relationship)


    # when we care a new task, completed_att should be NULL (NONE)







