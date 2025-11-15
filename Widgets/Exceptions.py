class FUIError(Exception):
    def __init__(self, statement='', cause=''):
        self.statement = statement
        self.cause = cause
        self.line = f"{self.statement}\n\tCause: {self.cause}"
        super().__init__(self.line)

    def __str__(self):
        return self.line
