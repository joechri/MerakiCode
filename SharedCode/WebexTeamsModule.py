import logging
from time import sleep

import requests
from dateutil.parser import parse as parse_dt
from requests_toolbelt.multipart.encoder import MultipartEncoder
from webexteamssdk import WebexTeamsAPI

logger = logging.getLogger()


class WebexTeams():

    def __init__(self, access_token, room_name):

        self.api = WebexTeamsAPI(access_token=access_token)
        self.room_name = room_name

        # get the existing rooms the bot is a member of
        existing_rooms = self.api.rooms.list(type='group')
        # find out if a room with the same name already exists
        for r in existing_rooms:
            if self.room_name == r.title:
                self.room_id = r.id
                break 

    def send_message(self, markdown, person_email=None, room_id=None, attachments=None):
        """
            Sends a message to the room
            Arguments:
                markdown (str):  Message text with optional markdown formatting
                room_name (str):  Room to send to
                attachments (card):  Adaptive card
                (https://dev-preview.webex.com/formatting-messages.html)
            Returns:
                Nothing
        """
        if not room_id:
            room_id = self.room_id

        if not person_email and not room_id:
            logger.warning('No person_email or room_id supplied, not sending message')
            return

        elif person_email and room_id:
            logger.warning('Both person_email AND room_id supplied, not sending message')
            return

        try:

            self.api.messages.create(
                roomId=room_id,
                toPersonEmail=person_email,
                markdown=markdown,
                attachments=attachments
            )

        except Exception as e:
            logger.warning(
                f'Exception occurred while trying to send message: {e}')

    def send_alert_details_card(self, data, person_email=None, room_id=None):
        alert_date = parse_dt(data['occurredAt']).strftime("%a %b %d %Y %I:%M %p")        
        card = {
            'contentType': 'application/vnd.microsoft.card.adaptive',
            'content': {
                '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
                'type': 'AdaptiveCard',
                'version': '1.2',
                'body': [
                    {
                        'type': 'TextBlock',
                        'text': 'Meraki Alert',
                        'size': 'Medium',
                        'weight': 'Bolder',
                        'wrap': True
                    },
                    {
                        'type': 'ColumnSet',
                        'columns': [
                            {
                                'type': 'Column',
                                'items': [
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Time of Alert:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Alert Severity:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Alert Type:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Org Name:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Org URL:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Network Name:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Network URL:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Hostname:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Model:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Device URL:'
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': 'Serial Number:'
                                    }
                                ]
                            },
                            {
                                'type': 'Column',
                                'items': [
                                    {
                                        'type': 'TextBlock',
                                        'text': alert_date
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['alertLevel']
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['alertType']
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['organizationName']
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['organizationUrl']
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['networkName']
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['networkUrl']
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['deviceName']
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['deviceModel']
                                    },
                                    {   'type': 'TextBlock',
                                        'text': f"[Device Link]({data['deviceUrl']})"
                                    },
                                    {
                                        'type': 'TextBlock',
                                        'text': data['deviceSerial']
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'actions': []
            }
        }

        self.send_message('Meraki Alert Card', person_email=person_email, room_id=room_id, attachments=[card])