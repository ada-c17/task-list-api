#####GRAVEYARD######
####################
######WAVE_1########
######routes########
## from task GET route
    # title_query = request.args.get("title")
    # is_complete = request.args.get("completed_at")

    # if title_query:
    #     tasks = Task.query.filer_by(title=title_query)
    # else:
    #     tasks = Task.query.filter_by(title=title_query)

    # if Task.completed_at == None:
    # change the key of completed_at to "is complete"
    # change value None == False
    # for task in tasks:
    #     if Task.completed_at == None:
    #         task["completed_at"] == task["is_complete"]
    #         task["is_complete"] == False
    #     else:
    #         Task.completed_at == is_complete
    #         task["completed_at"] == task["is_complete"]

######WAVE_2########
######routes########
## in get ##
    # print(sort_param)
    # asc or desc

    # order ascending:
    # need request to have asc
    # tasks_asc = Task.query.order_by(Task.title).all()
    # order descending:
    # need req to have desc
    # tasks_desc = Task.query.order_by(desc(Task.title)).all()


    ### this might query titles and need a change in task_response
    #   title_query = request.args.get("title")
    ### this might be an alternative
    # tasks = Task.query.all()
    
    # if title_query:
    #     tasks = Task.query.order_by(Task.title).all()
    # else:
    #     tasks = Task.query.all()


####################
########END#########
