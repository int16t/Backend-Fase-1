class NotFound(Exception):
    def __init__(self, name: str):
        self.name = name


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email

