import uuid
# DB
import mysql.connector as connector
from mysql.connector import errorcode
from datetime import datetime

from preference import Preference
from subject import Subject
from User_token import User_token
from rrError import SqlError

# debug
import pprint


class DataBaseConnector:

    def __init__(self):
        try:
            self.__db = connector.connect(
                host="127.0.0.1",
                user="root",
                password="password",
                port="3307",
                database="rental",
                auth_plugin='mysql_native_password')

            self.__cursor = self.__db.cursor()
            self.__create_subject_table()
            self.__create_user_info_table()
            self.__create_user_token_table()
            self.__create_user_preference_table()

        except connector.Error as error:
            print(error)
            print(error.msg)

    def __create_subject_table(self):
        query = """CREATE TABLE IF NOT EXISTS `rental_subjects` (
              `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
              `subject_id` varchar(10) NOT NULL,
              `name` varchar(255) NOT NULL DEFAULT '',
              `price` varchar(12) NOT NULL DEFAULT 0,
              `location` varchar(255) NOT NULL DEFAULT '',
              `sub_type` varchar(10) NOT NULL DEFAULT '',
              `size` varchar(10) NOT NULL DEFAULT '',
              `floor` varchar(20) NOT NULL DEFAULT '',
              `contact_person` varchar(255) NOT NULL DEFAULT '',
              `url` varchar(255) NOT NULL DEFAULT '',
              `created_at` datetime NOT NULL,
              `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              UNIQUE KEY `subject_id` (`subject_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__db._execute_query(query)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)

    def update_subject(self, subjects):
        sqlCommand = """
            INSERT INTO rental_subjects(
            subject_id, name, price, location, sub_type, size, floor, contact_person, url, created_at
            ) 
            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE 
            name=VALUES(name), 
            price=VALUES(price), 
            location=VALUES(location), 
            sub_type=VALUES(sub_type), 
            size=VALUES(size),
            floor=VALUES(floor),
            contact_person=VALUES(contact_person),
            url=VALUES(url),
            created_at=VALUES(created_at)
        """
        # %s, %s, %s, %s, %s, %s, %s, %s, %s
        # ?, ?, ?, ?, ?, ?, ?, ?, ?

        def mapping(datum):
            return (
                datum.subject_id,
                datum.name,
                datum.price,
                datum.location,
                datum.sub_type,
                datum.size,
                datum.floor,
                datum.contact_person,
                datum.url,
                datetime.now()
            )

        subjects = map(mapping, subjects)
        self.__cursor.executemany(sqlCommand, subjects)
        self.__db.commit()

    def drop_table(self):
        sqlCommand = """
        DROP TABLE rental_subjects
        """
        self.__execute_sql_command(sqlCommand)

    def clear_table(self):
        sqlCommand = """
        TRUNCATE TABLE rental_subjects
        """
        self.__execute_sql_command(sqlCommand)

    def __execute_sql_command(self, command: str):
        self.__db._execute_query(command)
        self.__db.commit()

    def __create_user_info_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user_info` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `name` varchar(255) NOT NULL,
              `email` varchar(255) NOT NULL,
              `password` varchar(255) NOT NULL,
              `phone` varchar(255) NOT NULL,
              `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              UNIQUE KEY `id` (`id`),
              UNIQUE KEY `email` (`email`),
              UNIQUE KEY `phone` (`phone`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__db._execute_query(query)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)

    def register_user(self, user_name, email, password, phone):
        sqlCommand = """
            INSERT INTO user_info(
                name, email, password, phone
            )
            VALUES(
                %s, %s, %s, %s
            )
        """

        try:
            data = (user_name, email, password, phone)
            self.__cursor.execute(sqlCommand, data)
            self.__db.commit()
            latest_user_id = str(self.__cursor.lastrowid)
            print(f"latest_user_id: {latest_user_id}")
            return latest_user_id
        except connector.Error as error:
            print(error)
            print(error.msg)
            return None

    def get_user_id(self, email):
        sqlCommand = """
            SELECT id, password
            FROM user_info
            WHERE email = %s
        """

        try:
            email = (email,)
            self.__cursor.execute(sqlCommand, email)
            result = self.__cursor.fetchall()
            if len(result) > 0:
                first_result = result[0]
                id = first_result[0]
                password_hash = first_result[1]
                self.__db.commit()
                return (id, password_hash)
            else:
                self.__db.commit()
                return None

        except connector.Error as error:
            print(error)
            print(error.msg)


    def __create_user_token_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user_token` (
              `id` varchar(36) NOT NULL,
              `device_token` varchar(255),
              `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              UNIQUE KEY `id` (`id`),
              UNIQUE KEY `device_token` (`device_token`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__db._execute_query(query)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)

    def get_user_token(self, user_id: str):
        sqlCommand = """
        SELECT device_token 
        FROM user_token
        WHERE id = %s
        """

        try:
            id = (user_id,)
            self.__cursor.execute(sqlCommand, id)
            result = self.__cursor.fetchall()
            if len(result) > 0:
                first_result = result[0]
                first_element = first_result[0]
                self.__db.commit()
                return first_element
            else:
                self.__db.commit()
                return None

        except connector.Error as error:
            print(error)
            print(error.msg)

    def update_user_token(self, user_token: User_token):
        sqlCommand = """
            INSERT INTO user_token(
                id, device_token
            )
            VALUES(
                %s, %s
            )
        """

        try:
            data = (user_token.user_id, user_token.device_token)
            self.__cursor.execute(sqlCommand, data)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)

    def __create_user_preference_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user_preference` (
              `id` int(11) unsigned NOT NULL ,
              `region` varchar(255),
              `kind` varchar(255),
              `rent_price` int(11) unsigned,
              `pattern` varchar(255),
              `space` varchar(255),
              `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__db._execute_query(query)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)

    def alter_table_preference(self):
        query = """
            ALTER TABLE user_preference
            ADD value varchar(255) NOT NULL DEFAULT '';
        """
        self.__execute_sql_command(query)

    def get_user_preference(self, user_id: str):
        sqlCommand = """
        SELECT type, value 
        FROM user_preference
        WHERE user_id = %s
        """

        try:
            id = (user_id,)
            self.__cursor.execute(sqlCommand, id)
            result = self.__cursor.fetchall()
            self.__db.commit()
            print(result)
            if len(result) > 0:
                # for element in result
                pres = []
                for element in result:
                    if len(element) == 2:
                        pref = Preference()
                        pres.append(Preference(
                            user_id, element[0], element[1]))
                    else:
                        raise TypeError
                return pres
            else:
                return None

        except connector.Error as error:
            print(error)
            print(error.msg)

    def update_user_preference(self, preference: Preference):
        print(f"{preference.sql_insert_field_string()}")
        # print(f"{",".join(['%s'] * preference.sql_insert_value_count())}")
        print(f"{preference.on_duplicate_key_update_string()}")
        sqlCommand = f"""
            INSERT INTO user_preference(
                {preference.sql_insert_field_string()}
            ) 
            VALUES(
                {preference.sql_insert_value_string()}
            )
            ON DUPLICATE KEY UPDATE 
            {preference.on_duplicate_key_update_string()}
        """
        print(sqlCommand)

        try:
            self.__execute_sql_command(sqlCommand)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)
            raise SqlError(error.msg)

    # retrive user's device token for push notification if subject match user's preference.
    def get_subscribe_user_from_subject(self, subject: Subject):
        sqlCommand = """
            
        """

        data = (subject.location, subject.sub_type)

        try:
            self.__cursor.execute(sqlCommand, data)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)
