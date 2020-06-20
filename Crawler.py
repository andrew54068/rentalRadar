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
    while 1:
        try:
            url = "https://rent.591.com.tw/?kind=0&region=1&order=posttime&orderType=desc"
            subjects = DataProvider.get_subjects_from_url(url)
            if subjects is not None:
                db.update_subject(subjects)
                manager = NotificationManager(db)
                
            else:
                print("subject is none.")
        except:
            raise AssertionError("Oops!", str(sys.exc_info()[1]), "occurred.")
        time.sleep(20)