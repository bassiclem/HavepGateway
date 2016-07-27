# Created by Saujan Ghimire 5-17-2016
import json
import pymysql


# ISensitGW API Class holding common funcitons for gateway Interaction


class ISensitGW:
    """
        Handle gateway configuration.
    """

    def __init__(self):
        """Initialise ISensitGW Class"""
        self.config_data = None

    # static methods do not receive first implicit argument--> self

    def init_json_config_data(self):
        """
        Initialise class via the json config file.
        :return: True if config file was found, Flase if not found.
        :rtype: Boolean
        """
        try:
            # TODO - change to absolute path for other systems
            with open('/home/pi/ISensitGateway/isensitgwapi/ISENSIT_GW.json', 'r') as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            print("File was not found")
            return False
        else:
            return True

    def get_gateway_name(self):
        """
        Return the current gateway name.
        :return: gateway id
        :rtype: string
        """
        return self.config_data['gatewayName'] + "_" + self.config_data['gatewayID']

    def get_post_url(self):
        """
        Return the AWS POST URL.
        :return: POST url
        :rtype: string
        """
        return self.config_data['post_url']

    def get_get_url(self):
        """
        Return the GET url of AWS.
        :return: aws url
        :rtype: str
        """
        return self.config_data['get_url']

    def get_gateway_id(self):
        """
        Return the gateway id
        :return: gateway id
        :rtype: int
        """
        return self.config_data['gatewayID']

    def get_aws_credentials(self):
        """
        Return SECRET KEY and ACCESS KEY for AWS
        :rtype: object
        """
        return self.config_data['awsCredentials']

    def get_software_version(self):
        """
        Retrun the Software Version
        :return: software version
        :rtype: string
        """
        return self.config_data['software_version']

    def get_mysql_credentials(self):
        """
        Return MySQL credentials, host, username and password
        :return: Host, Username, Password
        :rtype: object
        """
        return self.config_data['mysql_credentials']

    def get_mysql_sleeptime(self):
        """
        Return Sleeptime for BLE reading
        :return: sleeptime
        :rtype: int
        """
        return self.config_data['sleep_time']

    def set_software_version(self, version):
        """
        Set Gateway Software Version
        :param version: new version to set
        :type version: string
        """
        self.update_config_file('software_version', version)

    @staticmethod
    def update_config_file(item, value):
        """
        Update Config File
        :param item: Key for the config file
        :type item: String
        :param value: Value for the Key
        :type value: String
        :return: success status
        :rtype: string
        """
        with open('ISENSIT_GW.json', 'r+') as settingsData:
            settings = json.load(settingsData)
            settings[item] = value  # update the make of the first car

            settingsData.seek(0)  # rewind to beginning of file
            settingsData.write(json.dumps(settings, indent=2, sort_keys=True))  # write the updated version
            settingsData.truncate()  # truncate the remainder of the data in the file
            return "success"

