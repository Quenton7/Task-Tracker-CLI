The application runs from the CLI where the user has to mention a command followed by certain user inputs. The purpose of this code is to track what you need to do, what you have done, and what you are currently working on. 

The user is able to:
  - Add, Update, and Delete tasks
  - Mark a task as in progress or done
  - List all tasks, tasks that are done, tasks that are not done and tasks that are in progress

The code generates a json file in the desktop named as tracker.json which stores the details of the task in the format :- id , description, status, createdAt and updatedAt

Below are the commands that can be utilised:

    task-cli.py add <task description> # Creates a task with the task description
    
    task-cli.py update <task id> <updated task description> # Updates the task description for the first task with task id mentioned
    
    task-cli.py delete <task id> # Deletes the first task with task id mentioned
    
    task-cli.py mark-in-progress <task id> # Marks the status as in-progress for the first task with task id mentioned
    task-cli.py mark-done <task id> # Marks the status as done for the first task with task id mentioned
    
    task-cli.py list # Displays all the tasks
    task-cli.py list done # Displays all the tasks with status done
    task-cli.py list todo # Displays all the tasks with status todo
    task-cli.py list in-progress # Displays all the tasks with status in-progress

  Project Recieved from : https://roadmap.sh/projects/task-tracker
