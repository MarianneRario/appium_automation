import requests
import json

from pyngrok import ngrok

ngrok.set_auth_token("1zPTG1WnErhY0xAMuLlCD0QvD9V_6s51HNP5jKHWESukJh88P")

public_url = ngrok.connect(5000, bind_tls=True).public_url
print(public_url)


def ngrok_public_url(webhook_url):
    data = {"content": public_url, "username": "Ngrok Public Url"}

    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


def webhook(img_url, thread_id, url_extension, webhook_url):
    data = {"content": public_url + url_extension, "username": "Discord Webhook",
            "embeds": [
                {
                    "description": "Request output",
                    "title": f"Output for Thread ID {thread_id}",
                    "url": img_url
                }
            ]}

    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))
