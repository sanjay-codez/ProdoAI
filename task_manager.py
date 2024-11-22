import array
from datetime import datetime, timedelta  # Correct imports for datetime functionalities
import heapq
import pickle
from custom_map import CustomMap
from stack import Stack
import numpy as np

class TaskManager:
    def __init__(self, file_path="tasks.pkl", completed_tasks_file="completed_tasks.pkl"):
        self.tasks = CustomMap(file_path)
        self.tasks.load()
        print(f"DEBUG: Loaded tasks: {self.tasks.items()}")  # Debug
        self.completed_tasks = Stack()
        self.completed_tasks_file = completed_tasks_file
        self.completed_tasks.load_from_file(self.completed_tasks_file)
        self.action_items = []  # Min Heap for priority tasks

    def get_task_counts(self):
        """Calculate total open and closed tasks."""
        open_tasks = 0
        closed_tasks = len(self.completed_tasks.to_list())  # Length of stack converted to list

        for class_name, tasks in self.tasks.items():
            open_tasks += len(tasks)  # Count tasks per class

        # Use a NumPy array to create a 2D structure
        return np.array([[1, open_tasks], [2, closed_tasks]])  # 1 for open tasks, 2 for closed tasks

    def add_class(self, class_name):
        if class_name not in self.tasks.keys():
            self.tasks.add(class_name, None)

    def add_task(self, class_name, task_name, deadline=None):
        task = {"name": task_name, "deadline": str(deadline), "completed": False}
        if class_name not in self.tasks.keys():
            self.add_class(class_name)
        self.tasks.add(class_name, task)

        # Assign priority based on deadline or default far future
        if deadline:
            due_date = datetime.strptime(deadline, "%m/%d/%y %H:%M:%S")
        else:
            due_date = datetime.now() + timedelta(days=365 * 10)  # Far future for no deadline
        heapq.heappush(self.action_items, (due_date, task_name, class_name))
        self.save_all()

    def complete_task(self, class_name, task_name):
        tasks = self.tasks.get(class_name, [])
        task_to_complete = next((task for task in tasks if task["name"] == task_name), None)

        if task_to_complete:
            tasks.remove(task_to_complete)
            task_to_complete["completed"] = True
            self.completed_tasks.push({"class_name": class_name, "task_name": task_name})
            self.save_all()
            return True
        return False

    def delete_class(self, class_name):
        self.tasks.remove(class_name)

    def get_recently_completed_tasks(self):
        return self.completed_tasks.to_list()

    def save_all(self):
        self.tasks.save()
        self.completed_tasks.save_to_file(self.completed_tasks_file)

    def get_action_items(self):
        """Return a sorted list of all open tasks."""
        # Rebuild the heap for any new tasks
        self.action_items = []
        for class_name, tasks in self.tasks.items():
            for task in tasks:
                if not task.get("completed", False):
                    deadline = task.get("deadline")
                    if deadline:
                        due_date = datetime.strptime(deadline, "%m/%d/%y %H:%M:%S")
                    else:
                        due_date = datetime.now() + timedelta(days=365 * 10)  # Default far future
                    heapq.heappush(self.action_items, (due_date, task["name"], class_name))

        # Convert heap to a sorted list
        return [(item[1], item[2], item[0].strftime("%m/%d/%y %H:%M:%S")) for item in sorted(self.action_items)]
    def categorize_tasks(self):
        """Categorize tasks into Overdue, Today's, and Future."""
        now = datetime.now()
        categorized_tasks = {"overdue": [], "today": [], "future": []}

        for class_name, tasks in self.tasks.items():
            for task in tasks:
                deadline_str = task.get("deadline", None)
                if deadline_str:
                    deadline = datetime.strptime(deadline_str, "%m/%d/%y %H:%M:%S")
                    if deadline.date() < now.date():
                        categorized_tasks["overdue"].append((task["name"], class_name, deadline_str))
                    elif deadline.date() == now.date():
                        categorized_tasks["today"].append((task["name"], class_name, deadline_str))
                    else:
                        categorized_tasks["future"].append((task["name"], class_name, deadline_str))

        return categorized_tasks