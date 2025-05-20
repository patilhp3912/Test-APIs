class environment:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.variables = {}  # Key-value dictionary to store environment variables

    def add_variable(self, key, value):
        self.variables[key] = value

    def remove_variable(self, key):
        if key in self.variables:
            del self.variables[key]

    def get_variable(self, key):
        return self.variables.get(key, None)

    def __str__(self):
        return f"Environment: {self.name}, Description: {self.description}, Variables: {self.variables}"

    def __repr__(self):
        return f"Environment({self.name}, {self.description}, {self.variables})"