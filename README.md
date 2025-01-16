The application runs from the CLI where the user has to mention a command followed by certain user inputs. The purpose of this code is to track what you need to do, what you have done, and what you are currently working on. 

The user is able to:
  - Add, Update, and Delete tasks
  - Mark a task as in progress or done
  - List all tasks, tasks that are done, tasks that are not done and tasks that are in progress

The code generates a json file in the desktop named as tracker.json which stores the details of the task in the format :- id , description, status, createdAt and updatedAt

Below are the commands that can be utilised:
  task-cli.py add <task description>
  task-cli.py update <task id> <updated task description>
  task-cli.py delete <task id>
  task-cli.py mark-in-progress <task id>
  task-cli.py mark-done <task id>
  task-cli.py list
  task-cli.py list done
  task-cli.py list todo
  task-cli.py list in-progress

  Project Recieved from : https://roadmap.sh/projects/task-tracker
