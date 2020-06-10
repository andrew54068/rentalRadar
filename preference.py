class Preference:

    def __init__(self, user_id: str, type: int, value: str):
        self.user_id = user_id
        self.type = type
        self.value = value

    def __str__(self):
        return ("user_id: " + str(self.user_id) + "\n" +
        "type: " + str(self.type) + "\n" +
        "value: " + self.value)