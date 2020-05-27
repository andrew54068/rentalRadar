# env
from dotenv import load_dotenv
# load_dotenv(verbose=True)
import time

from DataBaseConnector import DataBaseConnector
import DataProvider as DataProvider

db = DataBaseConnector()
# db.alter_table()
# db.drop_table()
# db.clear_table()
while 1:
    url = "https://rent.591.com.tw/?kind=0&region=1&order=posttime&orderType=desc"
    subjects = DataProvider.get_subjects_from_url(url)
    db.update_subject(subjects)
    time.sleep(10 * 60)