from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    required_attributes = {
        "title": True, 
        "description" : True,
        "completed_at" : False,
        }

    # Instance Methods
    def self_to_dict_no_goal(self):
        instance_dict = dict(
            id=self.task_id,
            title=self.title,
            description=self.description
        )
        if self.completed_at:
            instance_dict["is_complete"] = True
        else:
            instance_dict["is_complete"] = False
        return instance_dict
    
    def self_to_dict_with_goal(self):
        instance_dict = dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            goal_id=self.goal_id
        )
        if self.completed_at:
            instance_dict["is_complete"] = True
        else:
            instance_dict["is_complete"] = False
        return instance_dict

    def update_self(self, data_dict):
        for key in data_dict.keys():
            if hasattr(self, key):
                setattr(self, key, data_dict[key])
            else:
                raise ValueError(key)


    # Class Methods
    

    @classmethod
    def create_from_dict(cls, data_dict):
        if "completed_at" not in data_dict.keys():
            data_dict["completed_at"] = None

        if data_dict.keys() == cls.required_attributes.keys():
            return cls(title=data_dict["title"],
                    description = data_dict["description"],
                    completed_at = data_dict["completed_at"]
            )
        
        else:
            remaining_keys= set(data_dict.keys())-set(cls.required_attributes.keys())
            response=list(remaining_keys)
            raise ValueError(response)

    @classmethod
    def return_class_name(cls):
        return "Task"
