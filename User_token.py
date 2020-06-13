class User_token:

    def __init__(self, user_id: str, device_token: str):
        self.user_id = user_id
        self.device_token = device_token

    def __str__(self):
        return ("user_id: " + str(self.user_id) + "\n" +
        "device_token: " + str(self.device_token))