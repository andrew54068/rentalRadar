from os.path import join, dirname
import time
import sys

from dotenv import load_dotenv
# from subject import Subject
from DataBaseConnector import DataBaseConnector
import DataProvider as DataProvider

from push_notification import NotificationManager

env_path = join(dirname(__file__), '.env.dev')
load_dotenv(dotenv_path=env_path, verbose=True)

def start_crawl(db: DataBaseConnector):
    try:
        while 1:
            url = "https://rent.591.com.tw/?kind=0&region=1&order=posttime&orderType=desc"
            subjects = DataProvider.get_subjects_from_url(url)
            manager = NotificationManager()
            if subjects != None:
                new_subjects = list(db.update_subject(subjects))
                # print(f"new_subjects: {new_subjects}")
                for subject in list(new_subjects):
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


if __name__ == '__main__':
    db = DataBaseConnector()
    start_crawl(db)
