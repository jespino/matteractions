import requests


def report_abuse(webhook_url, text, domain, team_name, post_id):
    resp = requests.post(webhook_url, json={
        "text": "Abuse reported in this message: {}/{}/pl/{}\n\nWith text:\n  > {}".format(domain, team_name, post_id, text)
    })
