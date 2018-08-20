import requests
import time


def remind(webhook_url, seconds, username, text, domain, team_name, post_id):
    time.sleep(seconds)
    resp = requests.post(webhook_url, json={
        "text": "Remember this post: {domain}/{team_name}/pl/{post_id}\n\nWith text\n  > {text}".format(
            domain=domain,
            team_name=team_name,
            post_id=post_id,
            text=text,
        ),
        "channel": "@{}".format(username)
    })
