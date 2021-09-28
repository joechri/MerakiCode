import logging

from dnacentersdk import DNACenterAPI

logger = logging.getLogger()


class DNAC():

    def __init__(
        self, username='devnetuser', password='Cisco123!', base_url='https://sandboxdnac.cisco.com:443', version='2.2.2.3'
    ):

        self.api = DNACenterAPI(username=username, password=password, base_url=base_url, version=version)

    def get_devices_for_card(self):

        device_list = self.api.devices.get_device_list()

        return [{'hostname': x['hostname'], 'id': x['id']} for x in device_list['response']]

    def get_device_details_for_card(self, d_id):

        d = self.api.devices.get_device_by_id(d_id)

        return d['response']

