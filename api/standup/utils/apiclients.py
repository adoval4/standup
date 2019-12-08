# utilities
import requests
import json


class SlackClient:

    @staticmethod
    def send_message(webhook_url, message):
        res = requests.post(webhook_url, json.dumps({'text': message}))
        if res.status_code == 200:
            return True
        return False



