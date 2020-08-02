import os
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
            self.__connection = connector.connect(
                host=os.getenv("DB_HOST"),
                user="root",
                password=os.getenv("MYSQL_SECRET"),
                port="3306",
                database='rental',
                auth_plugin='mysql_native_password')
            self.__cursor = self.__connection.cursor(buffered=False, dictionary=True)

            self.__create_database()

            self.__create_subject_table()
            self.__create_user_info_table()
            self.__create_user_token_table()
            print(f"create user token table")
            self.__create_user_preference_table()
            self.__connection.commit()

        except connector.Error as error:
            print(error.msg)

    def __create_database(self):
        query = """
        CREATE DATABASE IF NOT EXISTS rental;
        USE rental;
        """
        try:
            self.__execute_sql_command(query, multi=True)
        except connector.Error as error:
            print(error.msg)

    def __create_subject_table(self):
        query = """CREATE TABLE IF NOT EXISTS `rental_subjects` (
              `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
              `subject_id` varchar(10) NOT NULL,
              `name` varchar(255) NOT NULL DEFAULT '',
              `region` varchar(12) NOT NULL DEFAULT '',
              `section` varchar(12) NOT NULL DEFAULT '',
              `kind` varchar(15) NOT NULL DEFAULT '',
              `price` varchar(12) NOT NULL DEFAULT 0,
              `location` varchar(255) NOT NULL DEFAULT '',
              `sub_type` varchar(10) NOT NULL DEFAULT '',
              `pattern` varchar(12) NOT NULL DEFAULT '',
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
            self.__execute_sql_command(query)
        except connector.Error as error:
            print(error.msg)

    def update_subject(self, subjects):

        current_time = datetime.now()
        datetime_str = current_time.strftime("%Y/%m/%d %H:%M:%S")

        sqlCommand = """
            INSERT INTO rental_subjects(
            subject_id, name, region, section, kind, price, location, sub_type, size, floor, contact_person, url, created_at, updated_at
            ) 
            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE 
            name=VALUES(name), 
            region=VALUES(region),
            section=VALUES(section),
            kind=VALUES(kind),
            price=VALUES(price), 
            location=VALUES(location), 
            sub_type=VALUES(sub_type), 
            size=VALUES(size),
            floor=VALUES(floor),
            contact_person=VALUES(contact_person),
            url=VALUES(url),
            updated_at=VALUES(updated_at)
        """

        def mapping(datum):
            return (
                datum.subject_id,
                datum.name if datum.name != None else '',
                datum.region if datum.region != None else '',
                datum.section if datum.section != None else '',
                datum.kind if datum.kind != None else '',
                datum.price if datum.price != None else '',
                datum.location if datum.location != None else '',
                datum.sub_type if datum.sub_type != None else '',
                datum.size if datum.size != None else '',
                datum.floor if datum.floor != None else '',
                datum.contact_person if datum.contact_person != None else '',
                datum.url if datum.url != None else '',
                datetime_str,
                datetime_str
            )

        subjects = map(mapping, subjects)
        self.__cursor.executemany(sqlCommand, subjects)
        self.__connection.commit()


        sqlQuery = f"""
            SELECT *
            FROM rental_subjects
            WHERE created_at = '{datetime_str}';
        """

        sql_result = self.__get_sql_result(sqlQuery)

        def mapping_to_subject(datum):
            return Subject(datum['subject_id'],
                           datum['name'],
                           datum['region'],
                           datum['section'],
                           datum['kind'],
                           datum['price'],
                           datum['location'],
                           datum['sub_type'],
                           datum['pattern'],
                           datum['size'],
                           datum['floor'],
                           datum['contact_person'],
                           datum['url'])

        result = map(mapping_to_subject, sql_result)

        return result

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
            self.__execute_sql_command(query)
        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

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
            self.__cursor.execute(sqlCommand, data, multi=True)
            self.__connection.commit()
            latest_user_id = str(self.__cursor.lastrowid)
            print(f"latest_user_id: {latest_user_id}")
            return latest_user_id
        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    def get_user_id_with_password_hash(self, email):
        sqlCommand = """
            SELECT id, password
            FROM user_info
            WHERE email = %s
        """

        try:
            result = self.__get_sql_result(sqlCommand, email)
            if len(result) > 0:
                print(f"result: {result}")
                first_result = result[0]
                id = first_result['id']
                password_hash = first_result['password']
                return (id, password_hash)
            else:
                return None

        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    def __create_user_token_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user_token` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `user_id` varchar(36) NOT NULL,
              `fcm_token` varchar(255),
              `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              UNIQUE KEY `id` (`id`),
              UNIQUE KEY `fcm_token` (`fcm_token`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__execute_sql_command(query)
        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    def get_user_tokens(self, user_ids: list):
        if type(user_ids) != list:
            raise TypeError

        if len(user_ids) == 0:
            return []

        sqlCommand = f"""
        SELECT fcm_token
        FROM user_token
        WHERE user_id IN ({", ".join(user_ids)})
        """
        print(f"get user fcm_token: {sqlCommand}")
        try:
            query_result = self.__get_sql_result(sqlCommand)
            print(f"query_result: {query_result}")
            result = []
            for data in query_result:
                result.append(str(data['fcm_token']))
            return result

        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    def update_user_token(self, user_token: User_token):
        sqlCommand = """
            INSERT INTO user_token(
                user_id, fcm_token
            )
            VALUES(
                %s, %s
            )
        """

        try:
            data = (user_token.user_id, user_token.fcm_token)
            self.__cursor.execute(sqlCommand, data)
            self.__connection.commit()
        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    def alter_table_preference(self):
        query = """
            ALTER TABLE user_preference
            ADD section varchar(10)
        """
        self.__execute_sql_command(query)

    def __create_user_preference_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user_preference` (
              `id` int(11) unsigned NOT NULL ,
              `region` varchar(10) NOT NULL,
              `kind` varchar(10),
              `section` varchar(10),
              `rent_price` int(11) unsigned,
              `pattern` varchar(10),
              `space` varchar(10),
              `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__execute_sql_command(query)
        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    def get_user_preference(self, user_id: str):
        sqlCommand = f"""
        SELECT region, kind, rent_price, pattern, space
        FROM user_preference
        WHERE id = %s
        """

        try:
            id = (user_id,)
            result = self.__get_sql_result(sqlCommand, param=id)
            print(result)
            if len(result) > 0:
                # for element in result
                pres = []
                for element in result:
                    if len(element) == 5:
                        pref = Preference(
                            user_id=user_id, 
                            region=element['region'],
                            kind=element['kind'],
                            rent_price=element['rent_price'],
                            pattern=element['pattern'],
                            space=element['space'])
                        pres.append(pref)
                    else:
                        raise TypeError
                return pres
            else:
                return None

        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    def update_user_preference(self, preference: Preference):
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
        except connector.Error as error:
            print(error.msg)
            raise SqlError(error.msg)

    # retrive user's device token for push notification if subject match user's preference.
    def get_subscribe_user_from_subject(self, subject: Subject):
        sqlCommand = f"""
            SELECT id as user_id
            FROM user_preference
            WHERE 1
            {subject.query_condition_string()}
        """

        try:
            query_result = self.__get_sql_result(sqlCommand)
            result = []
            for data in query_result:
                if len(data) > 0:
                    result.append(str(data['user_id']))
            return result
        except connector.Error as error:
            print(error.msg)
            raise error


    def __execute_sql_command(self, command: str, multi=False):
        try:
            self.__cursor.execute(command, multi=multi)
            self.__connection.commit()
        except connector.Error as error:
            raise error

    def __get_sql_result(self, command: str, param=None):
        try: 
            self.__cursor.execute(command, params=param, multi=False)
            print(f"have unread result: {self.__cursor._have_unread_result()}")
            result = self.__cursor.fetchall()
            self.__connection.commit()
            return result
        except connector.Error as error:
            raise error