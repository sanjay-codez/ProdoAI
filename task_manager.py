from custom_map import CustomMap  # Import the CustomMap class

class TaskManager:
    def __init__(self, file_path="tasks.pkl"):
        self.tasks = CustomMap(file_path)
        self.tasks.load()  # Load tasks from the map file

    def add_class(self, class_name):
        if not self.tasks.get(class_name):
            self.tasks.add(class_name, [])
            self.tasks.save()

    def add_task(self, class_name, task_name, deadline=None):
        task = {"name": task_name, "deadline": str(deadline),
                "completed": False}  # Ensure deadline is stored as a string
        current_tasks = self.tasks.get(class_name, [])
        if not isinstance(current_tasks, list):
            current_tasks = []
        current_tasks.append(task)
        self.tasks.map[class_name] = current_tasks
        self.tasks.save()

    def complete_task(self, class_name, task_name):
        current_tasks = self.tasks.get(class_name, [])
        for task in current_tasks:
            if isinstance(task, dict) and task["name"] == task_name:
                task["completed"] = True
                self.tasks.map[class_name] = current_tasks
                self.tasks.save()
                return True
        return False

    def delete_class(self, class_name):
        self.tasks.remove(class_name)

    def remove_task(self, class_name, task_name):
        tasks = self.tasks.get(class_name, [])
        if not isinstance(tasks, list):
            return False  # If tasks are not a list, return False

        task_to_remove = None
        for task in tasks:
            if isinstance(task, dict) and task.get("name") == task_name:  # Check if task is a dict and match the name
                task_to_remove = task
                break

        if task_to_remove:
            tasks.remove(task_to_remove)
            if not tasks:  # If the class has no more tasks, remove the class
                self.tasks.remove(class_name)
            else:
                self.tasks.map[class_name] = tasks
            self.tasks.save()
            return True
        return False


