class SeatingInformation:
    def __init__(
        self,
        name: str,
        course_code: str,
        date: str,
        time: str,
        terminal: str,
        block: str,
    ):
        self.name = name
        self.course_code = course_code
        self.date = date
        self.time = time
        self.terminal = terminal
        self.block = block

    def __str__(self):
        return f"{self.__dict__}"
