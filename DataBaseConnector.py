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

    def __createTable(self):
        query = """CREATE TABLE IF NOT EXISTS `balances` (
              `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
              `subject_id` varchar(10) NOT NULL,
              `name` varchar(255) NOT NULL DEFAULT '',
              `price` varchar(10) NOT NULL DEFAULT '',
              `location` varchar(255) NOT NULL,
              `sub_type` varchar(10) NOT NULL,
              `size` varchar(5) NOT NULL,
              `floor` varchar(5) NOT NULL,
              `contact_person` varchar(255) NOT NULL,
              `url` varchar(255) NOT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `subject_id` (`subject_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
            INSERT INTO transactions(
            subject_id, 
            name, 
            price,
            location,
            sub_type,
            size,
            floor,
            contact_person,
            url
            ) 
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """

        def mapping(datum):
            return (
                datum.id,
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