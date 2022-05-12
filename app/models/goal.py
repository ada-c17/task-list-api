from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy= True)

    def to_dict(self):
        task_list = []
        for task in self.tasks:
            task_list.append(task.to_dict())

        return {
            'id': self.goal_id,
            'name': self.name,
            'tasks': self.task_list
        }

    # def to_dict(self):
    #     cars_list = []
    #     for car in self.cars:
    #         cars_list.append(car.to_dict_basic())


    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "team": self.team,
    #         "country": self.country,
    #         "handsome": self.handsome,
    #         "cars": cars_list
    #         #"num_cars": len(self.cars)          
    #     }