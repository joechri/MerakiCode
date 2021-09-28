import logging

from dnacentersdk import DNACenterAPI
from dnacentersdk.exceptions import ApiError

logger = logging.getLogger()


class DNAC():

    def __init__(self):

        self.api = DNACenterAPI()

    def get_devices_for_card(self):

        device_list = self.api.devices.get_device_list()

        return [{'hostname': x['hostname'], 'id': x['id']} for x in device_list['response'] if x['hostname']]

    def get_device_details_for_card(self, d_id):

        d = self.api.devices.get_device_by_id(d_id)

        return d['response']

    def get_device_config_for_card(self, d_id):

        try:

            d = self.api.devices.get_device_config_by_id(d_id)

            return d['response']

        except ApiError as e:

            if e.status_code == 501:
                logger.warning(f'ApiError getting config: {e}')
                return None
