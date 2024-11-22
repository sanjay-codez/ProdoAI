import pickle
from custom_map import CustomMap
from stack import Stack

class TaskManager:
    def __init__(self, file_path="tasks.pkl", completed_tasks_file="completed_tasks.pkl"):
        self.tasks = CustomMap(file_path)
        self.tasks.load()
        print(f"Tasks loaded: {self.tasks.items()}")  # Debug to confirm data
        self.completed_tasks = Stack()
        self.completed_tasks_file = completed_tasks_file
        self.completed_tasks.load_from_file(self.completed_tasks_file)  # Load completed tasks

    def add_class(self, class_name):
        if class_name not in self.tasks.keys():
            self.tasks.add(class_name, None)
            self.tasks.save()  # Persist changes immediately

    def add_task(self, class_name, task_name, deadline=None):
        task = {"name": task_name, "deadline": str(deadline), "completed": False}
        if not self.tasks.get(class_name):  # Ensure the class exists
            self.add_class(class_name)
        self.tasks.add(class_name, task)
        self.tasks.save()  # Persist changes immediately

    def complete_task(self, class_name, task_name):
        """Mark a task as completed and move it to the recently completed stack."""
        tasks = self.tasks.get(class_name, [])
        task_to_complete = None

        # Locate the task to complete
        for task in tasks:
            if task["name"] == task_name:
                task_to_complete = task
                break

        if task_to_complete:
            # Remove the task from the main list and mark it as completed
            self.tasks.remove_value(class_name, task_to_complete)
            task_to_complete["completed"] = True  # Mark as completed
            self.completed_tasks.push({"class_name": class_name, "task_name": task_name})  # Push to stack
            self.completed_tasks.save_to_file(self.completed_tasks_file)  # Save recently completed tasks

            # Ensure the subject persists even if no tasks remain
            if not self.tasks.get(class_name):
                self.tasks.add(class_name, None)
            return True  # Task successfully completed

        return False  # Task not found

    def delete_class(self, class_name):
        """Delete a class (subject) and all its tasks."""
        self.tasks.remove(class_name)

    def get_recently_completed_tasks(self):
        """Return a list of recently completed tasks."""
        return self.completed_tasks.to_list()

    def save_all(self):
        """Save all data, including tasks and recently completed tasks."""
        self.tasks.save()
        self.completed_tasks.save_to_file(self.completed_tasks_file)

    def load_all(self):
        """Load all data, including tasks and recently completed tasks."""
        self.tasks.load()
        self.completed_tasks.load_from_file(self.completed_tasks_file)
