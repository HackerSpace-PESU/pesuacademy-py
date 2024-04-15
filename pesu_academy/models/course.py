class Course:
    def __init__(self, code: str, title: str, _type: str, status: str):
        self.code = code
        self.title = title
        self.type = _type
        self.status = status

    def __str__(self):
        return f"{self.__dict__}"
