import bcrypt

from DataBaseConnector import DataBaseConnector


class PasswordChecher:

    def __init__(self, db: DataBaseConnector):
        self.db = db

    def check(self, email, password):
        id_with_hash = self.db.get_user_id_with_password_hash(email)
        if id_with_hash is None:
            return None
        else:
            if bcrypt.checkpw(str(password).encode('utf-8'), str(id_with_hash[1]).encode('utf-8')):
                print("It Matches!")
                return id_with_hash[0]
            else:
                print("It Does not Match :(")
                return None

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
