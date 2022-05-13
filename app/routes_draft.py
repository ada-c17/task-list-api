@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    # new_task = Task.create(request_body)

    #not sure if this is right logic/syntax, need to test
    # if new_task['completed_at'] is None:
    #     new_task['completed_at'] = new_task['is_complete']
    #     new_task['is_complete'] = False
    try:
        request_body["completed_at"]
        # new_task.completed_at
    except:
        request_body["is_complete"] = False
        new_task = Task.create_not_complete(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    #correct response body?
    # return make_response(jsonify(f"Book {new_task.title} successfully created", 201))
    return make_response(jsonify(f"Book successfully created", 201))




@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        request_body["description"]
        request_body["title"]
    except:
        return {"details": "Invalid data"}, 400

    try:
        request_body["is_complete"]
    except:
        request_body["is_complete"] = False

    if request_body["completed_at"]:

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at= request_body["completed_at"],
                        is_complete=True)


        db.session.add(new_task)
        db.session.commit()

        return {
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": new_task.is_complete
            }
        }, 201
    
    new_task = Task.create_not_complete(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
        }
    }, 201
    