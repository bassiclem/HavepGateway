#!usr/bin/python

import pymysql
from isensit_gw import ISensitGW


class ISensitGWMysql(object):
    def __init__(self):
        self.config_data = ISensitGW()
        self.config_data.init_json_config_data()
        self.table = self.config_data.get_mysql_credentials()['acc_beacon_table']
        self.connection = None
        self.gatewayID = self.config_data.get_gateway_name()
        self.sleeptime = self.config_data.get_mysql_sleeptime()

    def connect_to_db(self):
        try:
            self.connection = pymysql.connect(
                host=self.config_data.get_mysql_credentials()['hostname'],
                user=self.config_data.get_mysql_credentials()['username'],
                password=self.config_data.get_mysql_credentials()['password'],
                db=self.config_data.get_mysql_credentials()['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

        except pymysql.Error as e:
            print("Connection error: ", str(e))
            return False

        except Exception as e:
            print("Mysql error: ", str(e))
            return False

        else:
            return self.connection

    def close_db(self):
        if self.connection.open:
            self.connection.close()

    def get_cursor(self):
        if self.connection.open:
            return self.connection.cursor()

    def insert_beacon_data(self, beacon_uuid, beacon_major, beacon_minor, beacon_rssi):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO " + self.table + " VALUES (NULL, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
                cursor.execute(sql, (beacon_uuid, beacon_major, beacon_minor, beacon_rssi))

        except Exception as e:
            print("Error :", str(e))
            self.connection.rollback()
            return False

        else:
            self.connection.commit()

    # def set_table(self, table):
    #     self.table = self.config_data.get_mysql_credentials()[table]
    #
    # def get_first_row_id(self):
    #     return 0

    def read_beacon_data(self, row_count):
        self.table = self.config_data.get_mysql_credentials()['beacon_table']
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from " + self.table + " where row_count = %s", row_count)
        if cursor.rowcount > 0:
            return cursor.fetchone()
        else:
            return None

    def read_first_beacon_data(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute("SELECT * from " + self.table + " limit 1;")

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                print("cursor ", cursor.rowcount)
                return cursor.fetchone()
            else:
                return None

    def read_first_five_beacon_data(self, count):
        data = []
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute("SELECT * from " + self.table + " limit " + str(count) + ";")

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                data.append(cursor.fetchall())
                return data
            else:
                return None

    def __sizeof__(self):
        return super().__sizeof__()

    def delete_beacon_data(self, row_count):
        cursor = self.connection.cursor()
        delete_stmt = "DELETE FROM " + self.table + " WHERE row_count = %s"
        cursor.execute(delete_stmt, (row_count,))
        self.connection.commit()

    def insert_acc_beacon_data(self, beacon_id, beacon_accx, beacon_accy, beacon_accz, beacon_rssi):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO " + self.table + " VALUES (NULL, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
                cursor.execute(sql, (beacon_id, beacon_accx, beacon_accy, beacon_accz, beacon_rssi))

        except Exception as e:
            print("Error :", str(e))
            self.connection.rollback()
            return False

        else:
            self.connection.commit()

    def read_first_acc_beacon_data(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute("SELECT * from " + self.table + " limit 1;")

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()
            else:
                return None

    def delete_acc_beacon_data(self, row_count):
        cursor = self.connection.cursor()
        delete_stmt = "DELETE FROM " + self.table + " WHERE row_count = %s"
        # print delete_stmt, "  ", row_count
        cursor.execute(delete_stmt, (row_count,))
        self.connection.commit()

    def read_last_acc_beacon_data(self, beacon_id):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT * from " + self.table + " WHERE beacon_id = %s order by row_count desc limit 1;"
                cursor.execute(sql, beacon_id)

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()["beacon_accz"]
            else:
                return None

    def read_last_acc_beacon_total_data(self):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * from " + self.table + " order by row_count desc limit 1;"
                cursor.execute(sql)

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()
            else:
                return None

    def read_last_acc_beacon_degree(self, beacon_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * from " + self.table + " WHERE beacon_id = %s order by row_count desc limit 1;"
                cursor.execute(sql, beacon_id)

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()
            else:
                return None

    def get_data_count(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM " + self.table)
        return cursor.rowcount

    def get_first_row_count(self):
        self.table = self.config_data.get_mysql_credentials()['beacon_table']
        cursor = self.connection.cursor()
        cursor.execute("SELECT row_count FROM " + self.table)
        if cursor.rowcount > 0:
            return cursor.fetchone()
        else:
            return None

    def read_user_data(self, row_count):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from " + self.table + " where user_id = %s", row_count)
        return cursor.fetchone()

    def delete_user_data(self, row_count):
        cursor = self.connection.cursor()
        delete_stmt = "DELETE FROM " + self.table + " WHERE user_id %s"
        cursor.execute(delete_stmt, (row_count,))
        self.connection.commit()

    def is_connected(self):
        return self.connection
