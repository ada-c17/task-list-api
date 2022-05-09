from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    required_attributes = {
        "title": True, 
        }

    # Instance Methods
    def self_to_dict(self):
        instance_dict = dict(
            id=self.goal_id,
            title=self.title,
        )
        # if self.completed_at:
        #     instance_dict["is_complete"] = True
        # else:
        #     instance_dict["is_complete"] = False
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
        # if "completed_at" not in data_dict.keys():
        #     data_dict["completed_at"] = None

        if data_dict.keys() == cls.required_attributes.keys():
            return cls(title=data_dict["title"],
                    # description = data_dict["description"],
                    # completed_at = data_dict["completed_at"]
            )
        
        else:
            remaining_keys= set(data_dict.keys())-set(cls.required_attributes.keys())
            response=list(remaining_keys)
            raise ValueError(response)
