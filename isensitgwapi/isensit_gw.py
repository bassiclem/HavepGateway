# Created by Saujan Ghimire 5-17-2016
import json
import pymysql


# ISensitGW API Class holding common funcitons for gateway Interaction


class ISensitGW:
    def __init__(self):
        self.config_data = None

    # static methods do not receive first implicit argument--> self

    def init_json_config_data(self):
        try:
            # TODO - change to absolute path
            with open('/home/pi/ISensitGateway/isensitgwapi/ISENSIT_GW.json', 'r') as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            print("File was not found")
            return False
        else:
            return True

    def get_gateway_name(self):
        return self.config_data['gatewayName'] + "_" + self.config_data['gatewayID']

    def get_post_url(self):
        return self.config_data['post_url']

    def get_get_url(self):
        return self.config_data['get_url']

    def get_gateway_id(self):
        return self.config_data['gatewayID']

    def get_aws_credentials(self):
        return self.config_data['awsCredentials']

    def get_software_version(self):
        return self.config_data['software_version']

    def get_mysql_credentials(self):
        return self.config_data['mysql_credentials']

    def get_mysql_sleeptime(self):
        return self.config_data['sleep_time']

    def set_software_version(self, version):
        self.update_config_file('software_version', version)

    @staticmethod
    def update_config_file(item, value):
        with open('ISENSIT_GW.json', 'r+') as settingsData:
            settings = json.load(settingsData)
            settings[item] = value  # update the make of the first car

            settingsData.seek(0)  # rewind to beginning of file
            settingsData.write(json.dumps(settings, indent=2, sort_keys=True))  # write the updated version
            settingsData.truncate()  # truncate the remainder of the data in the file
            return "success"


class ISensitGWMysql:
    def __init__(self):
        self.config_data = None

    @staticmethod
    def connect_to_db():
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='saujan126',
                                     db='isensit',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`user_name`, `user_password`) VALUES (%s, %s)"
                cursor.execute(sql, ('test', 'very-secret'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `user_id`, `user_password` FROM `users` WHERE `user_name`=%s"
                cursor.execute(sql, ('test',))
                result = cursor.fetchone()

        finally:
            connection.close()
