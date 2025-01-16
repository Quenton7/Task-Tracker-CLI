import os                      # Import the os module to check if the file exists
import json                    # Import the json module to read and write JSON files
import sys                     # Import the sys module to read command-line arguments
from datetime import datetime  # Import the datetime module to get the current date and time

def create_json(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file and initialize with an empty dictionary
        with open(file_path, "w") as file:
            json.dump([], file)

def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("File exists but contains invalid JSON.")
        data = []  # Initialize an empty list in this case
    return data

def write_json(file_path, data):
    # Write the data to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def add_task(file_path, task):
    data = read_json(file_path)
    # Intialize the task ID
    if len(data) == 0:
        task_id = 1
    else:
        task_id = data[len(data)-1]["id"]+1
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get the current date and time
    updated_time = "" # Initialize the updated time
    new_task = { "id" : task_id, "description": task, "status" : "todo", "createdAt": created_time, "updatedAt": updated_time } # Create a new task
    data.append(new_task) 
    write_json(file_path, data)

def update_task(file_path, task_id, task):
    data = read_json(file_path)
    task_req = [x for x in data if x["id"] == int(task_id)] # Retrieve the task based on the task ID
    if not task_req:
        print("Task not found")
        return
    task_req = task_req[0]  # Get the task
    task_req["description"] = task  # Update the task description
    task_req["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_json(file_path, data)

def delete_task(file_path, task_id):
    data = read_json(file_path)
    task_req = [x for x in data if x["id"] == int(task_id)] # Retrieve the task based on the task ID
    if not task_req:
        print("Task not found")
        return
    task_req = task_req[0]  # Get the task
    data.remove(task_req) # Remove the task from the list
    write_json(file_path, data)

def mark_status(file_path, task_id, status):
    data = read_json(file_path) 
    task_req = [x for x in data if x["id"] == int(task_id)]
    if not task_req:
        print("Task not found")
        return
    task_req = task_req[0]
    task_req["status"] = status # Update the status of the task
    task_req["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_json(file_path, data)  

def list_tasks(file_path, status):
    data = read_json(file_path)
    if status:
        tasks = [x for x in data if x["status"] == status]
    else:
        tasks = data

    # Check if there are any tasks
    if tasks == []:
        print("No tasks found")
        return

    # Print the tasks
    for task in tasks:
        print("- Task ID:", task["id"])
        print("- Description:", task["description"])
        print("- Status:", task["status"])
        print("- Created At:", task["createdAt"])
        print("- Updated At:", task["updatedAt"])
        print()
    


if __name__ == "__main__":
    # Filepath of the JSON file
    file_path = r"C:\Users\user\OneDrive\Desktop\tracker.json"
    create_json(file_path)

    # Check if the user has provided any command
    if len(sys.argv) < 2:
        print("Usage: command [id optional] [task optional] [progress optional]")
        sys.exit(1)

    command = sys.argv[1].lower() # Retrieve the command
    match command:
        case "add": 
            # Check if the user has provided the task description
            if len(sys.argv) < 3:
                print("Task description is required")
                sys.exit(1)
            task = sys.argv[2] 
            add_task(file_path, task) # Add the task to the JSON file

        case "update":
            # Check if the user has provided the task ID and description
            if len(sys.argv) < 4:
                print("Task ID and description are required")
                sys.exit(1)
            task_id = sys.argv[2]
            task = sys.argv[3]
            update_task(file_path,task_id,task) # Update the task in the JSON file

        case "delete":
            # Check if the user has provided the task ID
            if len(sys.argv) < 3:
                print("Task ID is required")
                sys.exit(1)
            task_id = sys.argv[2]
            delete_task(file_path,task_id) # Delete the task from the JSON file

        case "list":
            # Check if the user has provided the status
            if len(sys.argv) == 2:
                status = "" # Retrieve all the tasks
            else:
                status = sys.argv[2] # Retrieve the tasks based on the status
            list_tasks(file_path,status) # List the tasks from the JSON file

        case "mark-in-progress":
            # Check if the user has provided the task ID
            if len(sys.argv) < 3:
                print("Task ID is required")
                sys.exit(1)
            task_id = sys.argv[2]
            mark_status(file_path,task_id,"in-progress") # Mark the task as in-progress

        case "mark-done":
            # Check if the user has provided the task ID
            if len(sys.argv) < 3:
                print("Task ID is required")
                sys.exit(1)
            task_id = sys.argv[2]
            mark_status(file_path,task_id,"done")   # Mark the task as done
        case _:
            print("Unknown task")    # Print an error message if the command is unknown
