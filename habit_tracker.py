import pickle
import os

class HabitNode:
    def __init__(self, name, frequency, streak=0, last_completed=None, target_streak=7, color="#1a1b4b", progress=0):
        self.name = name
        self.frequency = frequency
        self.streak = streak
        self.last_completed = last_completed
        self.target_streak = target_streak
        self.color = color
        self.progress = progress
        self.left = None
        self.right = None

class HabitTracker:
    def __init__(self, file_path="habits.pkl"):
        self.root = None
        self.file_path = file_path
        self.load()  # Load habits from file at initialization

    def add_habit(self, name, frequency, target_streak=7, color="#1a1b4b"):
        def _add(node, name, frequency):
            if not node:
                return HabitNode(name, frequency, target_streak=target_streak, color=color)
            if name < node.name:
                node.left = _add(node.left, name, frequency)
            elif name > node.name:
                node.right = _add(node.right, name, frequency)
            return node

        self.root = _add(self.root, name, frequency)
        self.save()  # Save changes after adding a habit

    def update_progress(self, name):
        node = self.find_habit(name)
        if node:
            node.streak += 1
            node.progress = min(100, (node.streak / node.target_streak) * 100)
            self.save()
            return True
        return False

    def save(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.root, file)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as file:
                self.root = pickle.load(file)
        else:
            self.root = None  # Initialize with an empty tree if file doesn't exist

    def find_habit(self, name):
        def _find(node, name):
            if not node:
                return None
            if name == node.name:
                return node
            elif name < node.name:
                return _find(node.left, name)
            else:
                return _find(node.right, name)

        return _find(self.root, name)

    def inorder_traversal(self):
        habits = []

        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            habits.append(node)
            _inorder(node.right)

        _inorder(self.root)
        return habits

    def remove_habit(self, name):
        def _remove(node, name):
            if not node:
                return None
            if name < node.name:
                node.left = _remove(node.left, name)
            elif name > node.name:
                node.right = _remove(node.right, name)
            else:
                # Node to delete found
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                # Node with two children: Get the inorder successor
                successor = node.right
                while successor.left:
                    successor = successor.left
                node.name, node.frequency, node.streak, node.target_streak, node.color, node.progress = \
                    successor.name, successor.frequency, successor.streak, successor.target_streak, successor.color, successor.progress
                node.right = _remove(node.right, successor.name)
            return node

        self.root = _remove(self.root, name)
        self.save()
        return True