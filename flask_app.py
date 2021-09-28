import json
from os import environ

import azure.functions as func
from flask import Flask, request, make_response

from HTTPWebexBot import main as main_http_func
from TimerCreateWebhooks import main as update_webhooks

app = Flask(__name__)


@app.route('/webexbot', methods=['POST'])
def proxy_call():

    r = func.HttpRequest(
        method=request.method,
        url=request.url,
        headers=request.headers,
        body=request.data
    )

    resp = main_http_func(r)

    return make_response(resp.get_body(), resp.status_code)


if __name__ == '__main__':

    # try the local flask config file
    try:
        with open('Flask_Config_Env.json') as json_file:
            json_data = json.load(json_file)

            environ.update(json_data)
    except FileNotFoundError:
        pass

    # try the azure function local settings file
    try:
        with open('local.settings.json') as json_file:
            json_data = json.load(json_file)

            environ.update(json_data['Values'])
    except FileNotFoundError:
        pass

    environ['RUNNING_AS_FLASK_APP'] = 'yes'

    class MockTimer():
        def __init__(self):
            self.past_due = False

    # update the webhooks
    update_webhooks(MockTimer())

    app.run()
