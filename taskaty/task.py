class Task:
    def __init__(
        self, title, description=None, start_date=None, end_date=None, done=False
    ):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.done = done

    def __str__(self):
        return f"{self.title}, {self.description}, {self.start_date}, {self.end_date}, {self.done}"
