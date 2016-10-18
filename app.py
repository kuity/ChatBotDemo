import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = ''
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]
                    send_message(sender_id, "got it, thanks!")

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    payload = messaging_event["postback"]["payload"]
                    if 'help' in payload:
                        send_message(sender_id, payload)

    return "ok", 200

def set_greeting():
    params = { "access_token": os.environ["PAGE_ACCESS_TOKEN"] }
    headers = { "Content-Type": "application/json" }
    data = json.dumps({
        "setting_type":"greeting",
        "greeting":{
            "text":"Hi {{user_first_name}}, welcome to Ice Cream Factory's bot"
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)
    log(r)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)
    # if r.result is not None:

def set_start():
    params = { "access_token": os.environ["PAGE_ACCESS_TOKEN"] }
    headers = { "Content-Type": "application/json" }
    data = json.dumps({
        "setting_type":"call_to_actions",
        "thread_state":"new_thread",
        "call_to_actions":[
            {
                "payload": "Hola~ How may I help you?"
            }
        ]
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)
    log("Displaying response of setting get-started button")
    log(r)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)
    # if r.result is not None:


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    set_greeting()
    set_start()
    # set_mainscreen()
    app.run(debug=True)
