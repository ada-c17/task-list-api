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

######WAVE_3########
######routes########

# "completed"
# create a patch route to tasks/<task_id>/mark_complete
# request body has an id and a completed_at 'null' value
# resposnse body is dictionary with task: as key and tasks as values
# > nested dictionary is_complete key == true

# PATCH on tasks/<task_id>/mark_complete
# "complete" on "completed task"
# request is ID and completed_at with a datetime value
# response is dictionary with key task and value tasks
# > nested dictionary is_complete == true


# if it is " not completed"
# > patch route to tasks/<task_id>/mark_incomplete 
# ** noticce how there are two routes, make two routes
# request body has an id and a "completed_at" attribute with datetime
# update makes response body:
# dictionary with task as key and tasks as values
# >nested dictionary is_complete == false
# completed_at (which is in the methods) is null/None

# patch on tasks/<task_id>/mark_incomplete


#wave 4
## slack message sent to task-notifications with
## "Someone just completed the task My Beautiful Task"
## need to use api key !!
# api_key (?) made in .env
# > no request body
# params : channel and text
# authorization : api_key
# patch -> sends to channel 'task-notifications'
# {"type": "text",
# "text": "Hello World!"}
####################
########END#########
