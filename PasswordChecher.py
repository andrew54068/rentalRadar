import bcrypt

from DataBaseConnector import DataBaseConnector


class PasswordChecher:

    def __init__(self, db: DataBaseConnector):
        self.db = db

    def check(self, email, password):
        (id, hashed_password) = self.db.get_user_id(email)
        if bcrypt.checkpw(str(password).encode('utf-8'), str(hashed_password).encode('utf-8')):
            print("It Matches!")
            return id
        else:
            print("It Does not Match :(")
            return None

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())