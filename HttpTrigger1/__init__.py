import json
import logging
import traceback
from os import environ

import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# config to run as a local script vs. function
if __name__ == '__main__':
    with open('local.settings.json') as json_file:
        json_data = json.load(json_file)

        environ.update(json_data['Values'])


    try:
        # get the ngrok tunnel
        r = requests.get('http://localhost:4040/api/tunnels')

        tunnels = r.json()

        ngrok_url = tunnels['tunnels'][0]['public_url']

    except Exception:
        ngrok_url = None

    print()
