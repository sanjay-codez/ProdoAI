import pickle

class CustomMap:
    def __init__(self, file_path="map.pkl"):
        self.file_path = file_path
        self.map = {}

    def add(self, key, value):
        """Add a key-value pair to the map."""
        if key not in self.map:
            self.map[key] = []  # Initialize with an empty list if not present
        if value is not None:
            self.map[key].append(value)
        self.save()

    def get(self, key, default=None):
        """Retrieve the value for a key, or return the default value if the key does not exist."""
        return self.map.get(key, default)

    def remove(self, key):
        """Remove a key and all associated values from the map."""
        if key in self.map:
            del self.map[key]
            self.save()

    def remove_value(self, key, value):
        """Remove a specific value from a key."""
        if key in self.map and value in self.map[key]:
            self.map[key].remove(value)
            if not self.map[key]:  # Remove the key if the list is empty
                del self.map[key]
            self.save()

    def save(self):
        """Save the map to a file using pickle."""
        with open(self.file_path, "wb") as file:
            pickle.dump(self.map, file)

    def load(self):
        """Load the map from a file using pickle."""
        try:
            with open(self.file_path, "rb") as file:
                self.map = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.map = {}

    def keys(self):
        """Return the keys of the map."""
        return self.map.keys()

    def items(self):
        """Return the items of the map."""
        return self.map.items()

    def __iter__(self):
        """Allow iteration over the keys of the map."""
        return iter(self.map)

    def __getitem__(self, key):
        """Allow dict-like access to the map."""
        return self.get(key)
