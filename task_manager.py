from custom_map import CustomMap

class TaskManager:
    def __init__(self, file_path="tasks.pkl"):
        self.tasks = CustomMap(file_path)
        self.tasks.load()

    def add_class(self, class_name):
        if not self.tasks.get(class_name):  # Check if the class exists
            self.tasks.add(class_name, None)  # Initialize with an empty LinkedList

    def add_task(self, class_name, task_name, deadline=None):
        task = {"name": task_name, "deadline": str(deadline), "completed": False}
        if not self.tasks.get(class_name):  # Ensure the class exists
            self.add_class(class_name)
        self.tasks.add(class_name, task)

    def complete_task(self, class_name, task_name):
        tasks = self.tasks.get(class_name, [])
        for task in tasks:
            if task["name"] == task_name:
                task["completed"] = True
                break

    def delete_class(self, class_name):
        self.tasks.remove(class_name)

    def remove_task(self, class_name, task_name):
        tasks = self.tasks.get(class_name, [])
        for task in tasks:
            if task["name"] == task_name:
                self.tasks.remove_value(class_name, task)
                break
