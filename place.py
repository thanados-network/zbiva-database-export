class Place:
    def __init__(self):
        self.data = {}

    def lazy_initialize(self, key):
        """This method is called to initialize values lazily."""
        print(f"Lazily initializing value for '{key}'")
        return f"Computed value for {key}"

    def __getattr__(self, key):
        # If the key is not found in _data, lazily initialize it
        if key not in self._data:
            self._data[key] = self.lazy_initialize(key)
        return self._data[key]

    def __setattr__(self, key, value):
        # Ensure that normal attributes are handled correctly
        if key == "_data":
            super().__setattr__(key, value)
        else:
            # Set the key's value directly if provided
            self._data[key] = value

    def __repr__(self):
        return f"Site({self._data})"

