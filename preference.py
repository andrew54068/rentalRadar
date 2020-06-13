import json
from json import JSONEncoder

class Preference:

    def __init__(self, user_id: str, type: int, value: str):
        self.user_id = user_id
        self.type = type
        self.value = value

    def __str__(self):
        return ("user_id: " + str(self.user_id) + "\n" +
        "type: " + str(self.type) + "\n" +
        "value: " + self.value)

    def toJSON(self):
        # return json.dumps(self.__dict__)
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class PreferenceEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__