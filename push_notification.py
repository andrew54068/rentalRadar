# Send to single device.
from pyfcm import FCMNotification
from dotenv import load_dotenv
import os
import base64

from DataBaseConnector import DataBaseConnector
from subject import Subject

class NotificationManager:

    def send_push_notification(self, user_tokens, subject: Subject):

        fcm_api_key = os.getenv("FCM_API_KEY")
        # print(fcm_api_key)

        push_service = FCMNotification(api_key=fcm_api_key)

        # OR initialize with proxies

        push_service = FCMNotification(api_key=fcm_api_key)

        # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

        # registration_id = "cA53EyujqEHAr2VzhWi47M:APA91bGtXuVeilvlK7z3UrBTmRnBx7TRQphAm3_cjun6admjs_Apl2K34dNNC3Cgky35gxiCZ0akl9P3TFbzSUbPTTJK1aZhCwphjvh3194ksref_JKYdNNClrYq6EyCF3mz2f2kM1ja"
        # message_title = "rental alert"
        # message_body = "Hi john, your customized news for today is ready"
        # print("send notification")
        # result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        # Send to multiple devices by passing a list of ids.
        registration_ids = user_tokens

        temp = base64.b64decode(subject.name)
        name = temp.decode("UTF-8")

        message_title = f"{name}"
        message_body = f"{subject.location}/{subject.region}/{subject.location}/{subject.price}"
        data_message = {'subject_id': f'{subject.subject_id}'}
        
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)
        print(f"push result: {result}")