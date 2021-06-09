import pymysql


class MySQL:

    def __init__(self, credentials=None):

        self.sql_username = None
        self.sql_password = None
        self.sql_host = None
        self.sql_database = None
        self.sql_port = None
        self.connection = None
        # endregion

        if credentials:
            self.init_credentials(credentials)

    def __del__(self):
        if self.connection:
            if self.connection.open:
                self.connection.close()

    def init_credentials(self, credentials):

        self.sql_username = credentials["sql_username"]
        self.sql_password = credentials["sql_password"]
        self.sql_host = credentials["sql_host"]
        self.sql_database = credentials["sql_database"]
        self.sql_port = credentials["sql_port"]

    def connect(self):

        connection_db = {
            "host": self.sql_host,
            "user": self.sql_username,
            "database": self.sql_database,
            "port": self.sql_port
        }
        if self.sql_password:
            connection_db["passwd"] = self.sql_password

        connection = pymysql.connect(**connection_db)

        return connection

    @staticmethod
    def run_get_all(connection, sql):

        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

