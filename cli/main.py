import task_list

OPTIONS = {
        "1": "List all tasks", 
        "2": "Create a task",
        "3": "View one task", 
        "4": "Update task", 
        "5": "Delete task", 
        "6": "Mark complete",
        "7": "Mark incomplete",
        "8": "Delete all tasks",
        "9": "List all options",
        "10": "Quit"
        }

def list_options():

    for number, feature in OPTIONS.items():
        print(f"{number}. {feature}")


def make_choice():
    valid_choices = OPTIONS.keys()
    choice = None

    while choice not in valid_choices:
        print("\n What would you like to do? ")
        choice = input("Make your selection using the option number. Select 9 to list all options: ")

    return choice

def get_task_from_user(msg = "Input the id of the task you would like to work with: "):
    task = None
    tasks = task_list.list_tasks()
    if not tasks:
        task_list.print_stars("This option is not possible because there are no tasks.")
        return task
    count = 0
    help_count = 3 #number of tries before offering assistance
    while not task:
        id = input(msg)
        task = task_list.get_task(id)
        if not task:
            print_surround_stars("I cannot find that task.  Please try again.")
        count += 1
        if count >= help_count:
            print("You seem to be having trouble selecting a task.  Please choose from the following list of tasks.")
            print_all_tasks()
        
    return task

def print_task(task):
    print_single_row_of_stars()
    print("title: ", task["title"])
    print("description: ", task["description"])
    print("is_complete: ", task["is_complete"])
    print("id: ", task["id"])
    print_single_row_of_stars()

def print_all_tasks():
    tasks = task_list.list_tasks()
    print("\nTasks:")
    if not tasks:
        print_surround_stars("No tasks")
    else:
        for task in tasks:
            print_task(task)
    print_single_row_of_stars()

def print_surround_stars(sentence):
    print_single_row_of_stars()
    print(sentence)
    print_single_row_of_stars()

def print_single_row_of_stars():
    print("\n**************************\n")

def create_task():
    print("Great! Let's create a new task.")
    title=input("What is the title of your task? ")
    description=input("What is the description of your task? ")
    response = task_list.create_task(title, description)
    print_task(response)

def view_task():
    task = get_task_from_user("Input the id of the task you would like to select ")
    if task: 
        print("\nSelected Task:")
        print_task(task)

def edit_task():
    task = get_task_from_user()
    if task:
        title=input("What is the new title of your task? ")
        description=input("What is the new description of your task? ")
        response = task_list.update_task(task["id"], title, description)
        print("\nUpdated Task:")
        print_task(response)

def delete_task_ui():
    task = get_task_from_user("Input the id of the task you would like to delete: ")
    if task:
        task_list.delete_task(task["id"])
        print("\nTask has been deleted.")
        print_all_tasks()

def change_task_complete_status(status):
    status_text = "complete"
    if not status:
        status_text = "incomplete"
    task = get_task_from_user(f"Input the id of the task you would like to mark {status_text}: ")
    if task:
        if status:
            response = task_list.mark_complete(task["id"])
        else:
            response = task_list.mark_incomplete(task["id"])
        print(f"\nTask marked {status_text}:")
        print_task(response)

def delete_all_tasks():
    for task in task_list.list_tasks():
        task_list.delete_task(task["id"])
        print_surround_stars("Deleted all tasks.")

def run_cli():
    
    play = True
    while play:

        # get input and validate
        choice = make_choice()

        if choice=='1':
            print_all_tasks()
        elif choice=='2':
            create_task()
        elif choice=='3':
            view_task()
        elif choice=='4':
            edit_task()
        elif choice=='5':
            delete_task_ui()
        elif choice=='6':
            change_task_complete_status(True)
        elif choice=='7':
            change_task_complete_status(False)
        elif choice=='8':
            delete_all_tasks()
        elif choice=='9':
            list_options()
        elif choice=='10':
            play=False


print("Welcome to Task List CLI")
print("These are the actions you can take:")
print_single_row_of_stars()
list_options()
run_cli()

