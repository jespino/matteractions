import requests
from requests.auth import HTTPBasicAuth


def send_to_jira(api_url, api_user, api_token, project_key, text, type, summary):
    description = text
    if summary == "" or summary is None:
        summary = text[:150]

    if type == "" or type is None:
        type = "Bug"

    data = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": type}
        }
    }

    resp = requests.post("{}/rest/api/2/issue/".format(api_url),
                         json=data, auth=HTTPBasicAuth(api_user, api_token))
    return "{}/browse/{}".format(api_url, resp.json()['key'])
