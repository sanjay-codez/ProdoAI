import pickle

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def to_list(self):
        return self.stack.copy()  # Return a copy of the stack

    def save_to_file(self, file_path):
        """Save the stack to a file."""
        with open(file_path, "wb") as file:
            pickle.dump(self.stack, file)

    def load_from_file(self, file_path):
        """Load the stack from a file."""
        try:
            with open(file_path, "rb") as file:
                self.stack = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.stack = []  # Initialize an empty stack if the file is not found or empty
