from __future__ import print_function
import os
import sys
import json
import requests
from flask import Flask, request
import config
import icbot

app = Flask(__name__)
conf = []
state = config.default_state

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
    if data["object"] != "page":
        return "ok", 200

    for entry in data["entry"]:
        for messaging_event in entry["messaging"]:
            sender_id = messaging_event["sender"]["id"]
            hasMessage = messaging_event.get("message")
            hasText = "text" in messaging_event["message"]
            if hasMessage and hasText:
                message_text = messaging_event["message"]["text"]
                (r, state) = icbot.interpret(message_text, conf, state)
                for (body, resp_type) in r:
                    response = gen_resp(sender_id, body, resp_type)
                    send_message(response)
            elif hasMessage and not hasText:
                response = gen_resp(sender_id, "Sorry, I don't understand.", "text")
                send_message(response)
            if messaging_event.get("delivery"):
                pass
            if messaging_event.get("optin"):
                pass
            if messaging_event.get("postback"):
                payload = messaging_event["postback"]["payload"]
                if 'help' in payload:
                    response = gen_resp(sender_id, payload, "text")
                    send_message(response)

    return "ok", 200

def gen_resp(rid, text, rtype):
    assert(rtype in config.resp_types)
    if rtype == config.texttype:
        return json.dumps({ "recipient": { "id": rid },
                            "message"  : {"text": text}
                          })
    elif rtype == config.buymenu:
        return json.dumps
        ({ "recipient": { "id": rid },
          "message"  : 
            {"attachment":
                {"type":"template",
                 "payload":
                    {"template_type":"button",
                     "text":"What do you want to buy?",
                     "buttons":
                        [{
                          "type":"web_url",
                          "url":"https://haagendazs.com.sg/flavours/vanilla",
                          "title":"Vanilla Ice Cream"
                        },
                        {
                          "type":"web_url",
                          "url":"https://haagendazs.com.sg/flavours/chocolate-ice-cream",
                          "title":"Chocolate Ice Cream"
                        }]
                    }
                }
            }
        })
    return 0

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

def send_message(d):
    params = { "access_token": os.environ["PAGE_ACCESS_TOKEN"] }
    headers = { "Content-Type": "application/json" }
    data = d
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", 
                    params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()

if __name__ == '__main__':
    set_start()
    conf = icbot.parseConfig()
    app.run(debug=True)
