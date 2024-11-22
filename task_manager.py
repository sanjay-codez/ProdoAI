import pickle
from custom_map import CustomMap
from stack import Stack

class TaskManager:
    def __init__(self, file_path="tasks.pkl", completed_tasks_file="completed_tasks.pkl"):
        self.tasks = CustomMap(file_path)
        self.tasks.load()
        print(f"DEBUG: Loaded tasks: {self.tasks.items()}")  # Debug
        self.completed_tasks = Stack()
        self.completed_tasks_file = completed_tasks_file
        self.completed_tasks.load_from_file(self.completed_tasks_file)

    def add_class(self, class_name):
        if class_name not in self.tasks.keys():
            self.tasks.add(class_name, None)

    def add_task(self, class_name, task_name, deadline=None):
        task = {"name": task_name, "deadline": str(deadline), "completed": False}
        if class_name not in self.tasks.keys():
            self.add_class(class_name)
        self.tasks.add(class_name, task)

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
