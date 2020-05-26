# DB
import mysql.connector as connector
from mysql.connector import errorcode

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
            pprint.pprint("success")
            self.__createTable()
        except connector.Error as error:
            print(error)
            print(error.msg)
    
    def alter_table(self):
        query = """
            ALTER TABLE balances CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
            # alter table balances change `name` `name` varchar(255) character utf8;
        self.__execute_sql_command(query)

    def __createTable(self):
        query = """CREATE TABLE IF NOT EXISTS `balances` (
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
              PRIMARY KEY (`id`),
              UNIQUE KEY `subject_id` (`subject_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """
        try:
            self.__db._execute_query(query)
            self.__db.commit()
            pprint.pprint("success2")
        except connector.Error as error:
            print(error)
            print(error.msg)

    def update_subject(self, subjects):
        sqlCommand = """
            INSERT INTO balances(
            subject_id, name, price, location, sub_type, size, floor, contact_person, url
            ) 
            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE 
            name=VALUES(name), 
            price=VALUES(price), 
            location=VALUES(location), 
            sub_type=VALUES(sub_type), 
            size=VALUES(size),
            floor=VALUES(floor),
            contact_person=VALUES(contact_person),
            url=VALUES(url)
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
                datum.url
            )
        
        subjects = map(mapping, subjects)
        self.__cursor.executemany(sqlCommand, subjects)
        self.__db.commit()

    def drop_table(self):
        sqlCommand = """
        DROP TABLE balances
        """
        self.__execute_sql_command(sqlCommand)

    def clear_table(self):
        sqlCommand = """
        TRUNCATE TABLE balances
        """
        self.__execute_sql_command(sqlCommand)

    def __execute_sql_command(self, command: str):
        self.__db._execute_query(command)
        self.__db.commit()