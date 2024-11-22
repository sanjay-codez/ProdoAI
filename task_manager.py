from custom_map import CustomMap

class TaskManager:
    def __init__(self, file_path="tasks.pkl"):
        self.tasks = CustomMap(file_path)
        self.tasks.load()

    def add_class(self, class_name):
        """Add a new class (subject) to the task manager."""
        if class_name not in self.tasks.keys():  # Check if the class exists
            self.tasks.add(class_name, None)

    def add_task(self, class_name, task_name, deadline=None):
        """Add a task to the specified class."""
        task = {"name": task_name, "deadline": str(deadline), "completed": False}
        if not self.tasks.get(class_name):  # Ensure the class exists
            self.add_class(class_name)
        self.tasks.add(class_name, task)

    def complete_task(self, class_name, task_name):
        """Mark a task as completed."""
        tasks = self.tasks.get(class_name, [])
        for task in tasks:
            if task["name"] == task_name:
                task["completed"] = True
                break

    def delete_class(self, class_name):
        """Delete an entire class (subject)."""
        self.tasks.remove(class_name)

    def remove_task(self, class_name, task_name):
        """Remove a specific task from a class."""
        tasks = self.tasks.get(class_name, [])
        task_to_remove = None

        # Locate the task to remove
        for task in tasks:
            if task["name"] == task_name:
                task_to_remove = task
                break

        if task_to_remove:
            self.tasks.remove_value(class_name, task_to_remove)

        # Re-add the class if no tasks remain to prevent the class from being deleted
        if not self.tasks.get(class_name):
            self.tasks.add(class_name, None)

        return task_to_remove is not None  # Return whether a task was removed
