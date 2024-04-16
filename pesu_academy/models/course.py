from typing import Optional


class Attendance:
    def __init__(
            self,
            attended_classes: Optional[int] = None,
            total_classes: Optional[int] = None,
            percentage: Optional[float] = None
    ):
        self.attended_classes = attended_classes
        self.total_classes = total_classes
        self.percentage = percentage

    def __str__(self):
        return f"{self.__dict__}"


class Course:
    def __init__(self, code: str, title: str, _type: Optional[str] = None, status: Optional[str] = None,
                 attendance: Optional[Attendance] = None):
        self.code = code
        self.title = title
        self.type = _type
        self.status = status
        self.attendance = attendance

    def __str__(self):
        return f"{self.__dict__}"
