# Send to single device.
from pyfcm import FCMNotification
from dotenv import load_dotenv
import os

from DataBaseConnector import DataBaseConnector
from subject import Subject

class NotificationManager:

    def __init__(self, db):
        self.db = db

    # def handleNewSubjects(self, subjects: [Subject]):
        

    def __send_push_notification(self, ids):

        # get user token
        user_id = "fa210389-a8f6-402c-8681-ce8b628fbd89"
        user_token = self.db.get_user_token(user_id)
        print(user_token)

        fcm_api_key = os.getenv("FCM_API_KEY")
        print(fcm_api_key)

        push_service = FCMNotification(api_key=fcm_api_key)

        # OR initialize with proxies

        proxy_dict = {}
        push_service = FCMNotification(api_key=fcm_api_key, proxy_dict=proxy_dict)

        # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

        registration_id = "cA53EyujqEHAr2VzhWi47M:APA91bGtXuVeilvlK7z3UrBTmRnBx7TRQphAm3_cjun6admjs_Apl2K34dNNC3Cgky35gxiCZ0akl9P3TFbzSUbPTTJK1aZhCwphjvh3194ksref_JKYdNNClrYq6EyCF3mz2f2kM1ja"
        message_title = "rental alert"
        message_body = "Hi john, your customized news for today is ready"
        print("send notification")
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        # Send to multiple devices by passing a list of ids.
        # registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
        # message_title = "Uber update"
        # message_body = "Hope you're having fun this weekend, don't forget to check today's news"
        # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

        print(result)