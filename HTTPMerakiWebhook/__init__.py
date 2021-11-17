import logging
import traceback
from os import environ

import azure.functions as func

from SharedCode.WebexTeamsModule import WebexTeams

def main(req: func.HttpRequest) -> func.HttpResponse:

    logger = logging.getLogger()
    log_level = logging.getLevelName(environ['logging_level'])
    logger.setLevel(log_level)

    try:
        data = req.get_json()
        teams_api = WebexTeams(environ['WEBEX_TEAMS_ACCESS_TOKEN'],environ['WEBEX_TEAMS_ROOM_NAME'])
        
        teams_api.send_alert_details_card(data)

        return func.HttpResponse('Done', mimetype='text/html')

    except Exception as e:
        logger.critical(f'Exception: {e}')
        logger.critical(traceback.print_exc())

        raise e