from dotenv import load_dotenv
# load_dotenv(verbose=True)
import time
import sys

import DataBaseConnector as DataBaseConnector
import DataProvider as DataProvider

from preference import Preference
from push_notification import NotificationManager

# db = DataBaseConnector()
# db.alter_table_preference()
# db.alter_table()
# db.drop_table()
# db.clear_table()

def start_crawl(db: DataBaseConnector):
    try:
        while 1: 
            url = "https://rent.591.com.tw/?kind=0&region=1&order=posttime&orderType=desc"
            subjects = DataProvider.get_subjects_from_url(url)
            manager = NotificationManager()
            if subjects is not None:
                new_subjects = list(db.update_subject(subjects))
                # print(f"new_subjects: {new_subjects}")
                for subject in list(new_subjects)[0:1]:
                    # print(f"subject: {subject}")

                    user_ids = db.get_subscribe_user_from_subject(subject)
                    # print(f"{len(user_ids) > 0}")
                    if len(user_ids) > 0:
                        print(f"user_ids: {user_ids}")
                        user_tokens = db.get_user_tokens(user_ids)
                        if len(user_tokens) > 0:
                            print(f"user_tokens: {user_tokens}")
                            manager.send_push_notification(user_tokens, subject)

            else:
                print("subject is none.")
            time.sleep(20)
    except:
        raise AssertionError("Oops!", str(sys.exc_info()[1]), "occurred.")
