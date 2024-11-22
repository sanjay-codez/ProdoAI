from linked_list import LinkedList  # Import the LinkedList class
import pickle

class CustomMap:
    def __init__(self, file_path="map.pkl"):
        self.file_path = file_path
        self.map = {}

    def add(self, key, value):
        """Add a key-value pair to the map."""
        if key not in self.map or not isinstance(self.map[key], LinkedList):
            self.map[key] = LinkedList()  # Initialize a LinkedList if not present
        if value is not None:  # Only append if value is not None
            self.map[key].append(value)
        self.save()

    def get(self, key, default=None):
        """Retrieve the value for a key, or return the default value if the key does not exist."""
        if key in self.map and isinstance(self.map[key], LinkedList):
            return self.map[key].to_list()  # Convert LinkedList to list for use
        return default

    def remove(self, key):
        """Remove a key (and all associated values) from the map."""
        if key in self.map:
            del self.map[key]
            self.save()

    def remove_value(self, key, value):
        """Remove a specific value from a key."""
        if key in self.map and isinstance(self.map[key], LinkedList):
            self.map[key].remove(value)
            if self.map[key].is_empty():  # If the list is empty, remove the key
                del self.map[key]
            self.save()

    def save(self):
        """Save the map to a file using pickle."""
        serializable_map = {key: node.to_list() for key, node in self.map.items()}
        with open(self.file_path, "wb") as file:
            pickle.dump(serializable_map, file)

    def load(self):
        """Load the map from a file using pickle."""
        try:
            with open(self.file_path, "rb") as file:
                serializable_map = pickle.load(file)
            self.map = {key: LinkedList().from_list(values) for key, values in serializable_map.items()}
        except (FileNotFoundError, EOFError):
            self.map = {}

    def keys(self):
        """Return the keys of the map."""
        return self.map.keys()

    def items(self):
        """Return the items of the map as (key, list) tuples."""
        return {key: node.to_list() for key, node in self.map.items()}.items()

    def __iter__(self):
        """Allow iteration over the keys of the map."""
        return iter(self.map)

    def __getitem__(self, key):
        """Allow dict-like access to the map."""
        return self.get(key)
