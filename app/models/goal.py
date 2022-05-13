from app import db
from app.helper_functions import get_record_by_id


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    required_attributes = {
        "title" : True
        # "tasks" : False
    }

    # Instance Methods

    # I wanted to find a way to combine these two, but I couldn't get it to differentiate between when there was no self.tasks at all
    # and when self.tasks was already set to an empty list. So if you have any ideas I'd love to hear them!
    
    def self_to_dict_no_tasks(self):
        instance_dict = dict(
            id=self.goal_id,
            title=self.title
        )
        return instance_dict

    def self_to_dict_with_tasks(self):
        task_list = [task.self_to_dict() for task in self.tasks]
        instance_dict = dict(
            id=self.goal_id,
            title=self.title,
            tasks=task_list if task_list else []
        )
        return instance_dict

    def update_self(self, data_dict):
        dict_key_errors = []
        for key in data_dict.keys():
            if hasattr(self, key):
                setattr(self, key, data_dict[key])
            else:
                dict_key_errors.append(key)
        if dict_key_errors:
            raise ValueError(dict_key_errors)
    
    def return_id_and_task_ids_only(self):
        task_ids = [task.task_id for task in self.tasks]

        id_and_tasks_dict = dict(
            id=self.goal_id,
            task_ids = task_ids
        )
        return id_and_tasks_dict


    # Class Methods

    @classmethod
    def create_from_dict(cls, data_dict):
        ### future refactoring
        ### I'd like to add functionality here that would allow a goal to be created with task IDs in the input dict
        ### but I'm not sure I'll have time
        ### I could use below but I'd have to import Task and I'm not sure that's best practice
        # if "tasks" not in data_dict.keys():
        #   data_dict["tasks"] = []
        # new_instance = cls(title=data_dict["title"])
        # for elem in data_dict["task_ids"]:
        #     task = get_record_by_id(Task, elem)
        #     new_instance.tasks.append(task)

        if data_dict.keys() == cls.required_attributes.keys():
            return cls(title=data_dict["title"])
        else:
            remaining_keys= set(data_dict.keys())-set("title")
            response=list(remaining_keys)
            raise ValueError(response)
    
    @classmethod
    def return_class_name(cls):
        return "Goal"
