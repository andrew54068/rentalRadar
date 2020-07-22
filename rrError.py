class SqlError(Exception):

    def __init__(self, message="Salary != in (5000, 15000) range"):
        self.message = message
        super().__init__(self.message)