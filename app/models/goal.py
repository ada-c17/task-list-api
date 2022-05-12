from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy= True)

    def to_dict(self):
        return {
                'id': self.goal_id,
                'title': self.title}

        task_list = []
        for task in self.tasks:
            task_list.append(task.to_dict())
        if self.tasks:
            return {
                'id': self.goal_id,
                'title': self.title,
                'tasks': task_list}
        else:
            return {
                'id': self.goal_id,
                'title': self.title}


    # Examples helper functions:
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