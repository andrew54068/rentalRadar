class User_token:

    def __init__(self, user_id: str, fcm_token: str):
        self.user_id = user_id
        self.fcm_token = fcm_token

    def __str__(self):
        return ("user_id: " + str(self.user_id) + "\n" +
        "fcm_token: " + str(self.fcm_token))