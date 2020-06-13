# DB
import mysql.connector as connector
from mysql.connector import errorcode
from datetime import datetime

from preference import Preference

# debug
import pprint

class DataBaseConnector:

    def __init__(self):
        try:
            self.__db = connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "password",
                port = "3307",
                database = "rental",
                auth_plugin = 'mysql_native_password')

            self.__cursor = self.__db.cursor()
            self.__create_subject_table()
            self.__create_user_table()
            self.__create_user_preference_table()

        except connector.Error as error:
            print(error)
            print(error.msg)
    
    def alter_table(self):
        query = """
            ALTER TABLE rental_subjects
            DROP COLUMN value;
        """
            # ADD 
            #     created_at datetime NOT NULL DEFAULT NOW();
                # updated_at datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
            # alter table rental_subjects change `name` `name` varchar(255) character utf8;
        self.__execute_sql_command(query)

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

    def __create_user_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user` (
              `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
              `name` varchar(255) NOT NULL,
              `email` varchar(255),
              `phone` varchar(20),
              `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              UNIQUE KEY `id` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__db._execute_query(query)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)

    def __create_user_preference_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user_preference` (
              `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
              `type` int(3) unsigned NOT NULL,
              `user_id` int(11) unsigned,
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

    
    def update_user_preference(self, preferences: [Preference]):
        sqlCommand = """
            INSERT INTO user_preference(
            user_id, type, value
            ) 
            VALUES(
                %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE 
            user_id=VALUES(user_id), 
            type=VALUES(type),
            value=VALUES(value)
        """

        def mapping(datum):
            return (
                datum.user_id,
                datum.type,
                datum.value
            )
        
        preferences = map(mapping, preferences)

        try:
            self.__cursor.executemany(sqlCommand, preferences)
            self.__db.commit()
        except connector.Error as error:
            print(error)
            print(error.msg)