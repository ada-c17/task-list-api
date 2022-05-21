import task_list

OPTIONS = {
        "1": "View all", 
        "2": "Create",
        "3": "View one", 
        "4": "Update", 
        "5": "Delete", 
        "6": "Mark complete",
        "7": "Mark incomplete",
        "8": "Delete all",
        "9": "List all options",
        "10": "Quit",
        "A": "Assign task(s) to goal" 
        }

def list_options():

    for number, feature in OPTIONS.items():
        print(f"{number}. {feature}")


def make_choice():
    valid_choices = OPTIONS.keys()
    valid_resources = {'t', 'g'}
    choice = None
    resource = None

    while choice not in valid_choices:
        print("\n What would you like to do? ")
        choice = input("Make your selection using the option number. "
                        "Select 9 to list all options: ").upper()
    
    if choice == 'A':
        resource = 'g'
    elif choice in {'6', '7', '9', '10'}:
        resource = 't'
    while resource not in valid_resources:
        resource = input('Ok, are we working with tasks or goals? '
                        '(Enter "T" or "G"): ').lower()
            
    return choice, resource

def get_id_from_user(resource, msg = "Input the id of the item you would like to work with: "):
    item = None
    items = task_list.list_tasks() if resource == 't' else task_list.list_goals()
    if not items:
        task_list.print_stars("This option is not possible because there are none found.")
        return
    count = 0
    help_count = 3 #number of tries before offering assistance
    while not item:
        id = input(msg)
        item = task_list.get_task(id) if resource == 't' else task_list.get_goal(id)
        if not item:
            print_surround_stars("I cannot find that item.  Please try again.")
        count += 1
        if count >= help_count:
            print("You seem to be having trouble selecting an item.  Please choose from the following list.")
            print_all(resource)
        
    return item

def print_item(item):
    print_single_row_of_stars()
    for key in item:
        print(f'{key}: {item[key]}')
    print_single_row_of_stars()

def print_all(resource):
    if resource == 't': 
        items = task_list.list_tasks()
        print("\nTasks:")
    else:
        items = task_list.list_goals()
        print("\nGoals:")
    if not items:
        print_surround_stars("None found")
    else:
        for item in items:
            print_item(item)
    print_single_row_of_stars()

def print_surround_stars(sentence):
    print_single_row_of_stars()
    print(sentence)
    print_single_row_of_stars()

def print_single_row_of_stars():
    print("\n**************************\n")

def create(resource):
    print("Great! Let's create a new resource.")
    title=input("What is its title? ")
    if resource == 't':
        description=input("What is the description of your task? ")
        response = task_list.create_task(title, description)
    else:
        response = task_list.create_goal(title)
    print_item(response)

def view(resource):
    item = get_id_from_user(resource, "Input the id of the task you would like to select ")
    if item: 
        print("\nSelected Item:")
        print_item(item)

def edit(resource):
    item = get_id_from_user(resource)
    if item:
        title=input("What is the new title? ")
        if resource == 't':
            description=input("What is the new description of your task? ")
            response = task_list.update_task(item["id"], title, description)
            print("\nUpdated Task:")
        else:
            response = task_list.update_goal(item["id"], title)
            print("\nUpdated Goal:")
        print_item(response)

def delete(resource):
    item = get_id_from_user(resource, "Input the id of the item you would like to delete: ")
    if item:
        if resource == 't':
            task_list.delete_task(item["id"])
        else:
            task_list.delete_goal(item["id"])
        print("\nItem has been deleted.")
        print_all(resource)

def change_task_complete_status(status):
    status_text = "complete"
    if not status:
        status_text = "incomplete"
    task = get_id_from_user('t', f"Input the id of the task you would like to mark {status_text}: ")
    if task:
        if status:
            response = task_list.mark_complete(task["id"])
        else:
            response = task_list.mark_incomplete(task["id"])
        print(f"\nTask marked {status_text}:")
        print_item(response)

def delete_all(resource):
    if resource == 't':
        methods = ['list_tasks', 'delete_task']
    else:
        methods = ['list_goals', 'delete_goal']
    for item in getattr(task_list, methods[0])():
        getattr(task_list, methods[1])(item["id"])
        print_surround_stars("Deleted all items.")

def assign_to_goal():
    goal = get_id_from_user('g', f"Input the id of the goal you would like to assign tasks to: ")
    task_ids = input('Input the ids of the tasks you would like to assign, separated by spaces (ex: "1 2 3"): ').split()
    response = task_list.assign_tasks_to_goal(goal['id'], task_ids)

    print_item(goal)

def run_cli():
    
    play = True
    while play:

        # get input and validate
        choice = make_choice()

        if choice[0]=='1':
            print_all(choice[1])
        elif choice[0]=='2':
            create(choice[1])
        elif choice[0]=='3':
            view(choice[1])
        elif choice[0]=='4':
            edit(choice[1])
        elif choice[0]=='5':
            delete(choice[1])
        elif choice[0]=='6':
            change_task_complete_status(True)
        elif choice[0]=='7':
            change_task_complete_status(False)
        elif choice[0]=='8':
            delete_all(choice[1])
        elif choice[0]=='9':
            list_options()
        elif choice[0]=='10':
            play=False
        elif choice[0]=='A':
            assign_to_goal()


print("Welcome to Task List CLI")
print("These are the actions you can take:")
print_single_row_of_stars()
list_options()
run_cli()