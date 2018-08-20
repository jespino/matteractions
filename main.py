import json
import configparser
import os
from multiprocessing import Process
import hashlib
from functools import wraps

from flask import Flask
app = Flask(__name__)
from flask import request
from flask import jsonify, abort
from flask_wtf import CSRFProtect

from actions.deepmoji import suggest_emoji
from actions.abuse import report_abuse
from actions.translate import translate
from actions.remind import remind
from actions.autotag import autotag
from actions.autocorrect import autocorrect
from actions.trello_send import send_to_trello
from actions.jira_send import send_to_jira

csrf = CSRFProtect(app)

config = configparser.ConfigParser()
config.read("config.ini")


def get_config(action, key, default_value):
    value = os.environ.get("MMACTIONS_{}_{}".format(action.upper(), key.upper()), None)
    if value is None:
        value = config.get(action, key, fallback=default_value)
    if value == "true":
        return True
    elif value == "false":
        return False
    if action == "main" and key == "port":
        return int(value)
    return value


def check_enabled(action):
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):
            if not get_config(action, "enabled", False):
                return abort(404)
            return f(*args, **kwargs)
        return func
    return decorator


def check_signature(action):
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):
            key = get_config(action, "key", "").encode("utf-8")
            signature = request.headers.get('X-Action-Signature')
            if signature != hashlib.sha256(request.data+key).hexdigest():
                return abort(400)
            return f(*args, **kwargs)
        return func
    return decorator


@app.route("/deepmoji", methods=["POST"])
@csrf.exempt
@check_signature("deepmoji")
@check_enabled("deepmoji")
def deepmoji():
    r = request.data
    req = json.loads(r.decode())
    emoji = suggest_emoji(req['text'])
    if emoji is None:
        return jsonify(text="No reaction found", type='system_ephemeral', channel_id=req['channel_id'])
    return jsonify([
        {"text": emoji, "response_type": 'reaction'}
    ])


@app.route("/send-to-trello", methods=["POST"])
@csrf.exempt
@check_signature("send-to-trello")
@check_enabled("send-to-trello")
def send_to_trello_action():
    r = request.data
    req = json.loads(r.decode())
    cfg = config["send-to-trello"]
    url = send_to_trello(
        cfg["api_key"], cfg["api_token"], req['text'], cfg["board"])
    return jsonify([
        {"text": "Trello ticket created here: {}".format(
            url), "type": 'system_ephemeral', "channel_id": req['channel_id']}
    ])


@app.route("/send-to-jira", methods=["POST"])
@csrf.exempt
@check_signature("send-to-jira")
@check_enabled("send-to-jira")
def send_to_jira_action():
    r = request.data
    req = json.loads(r.decode())
    cfg = config["send-to-jira"]
    url = send_to_jira(cfg["api_url"], cfg["api_user"], cfg["api_token"], cfg["project_key"],
                       req['text'], req['extra_data'].get('type', ''), req['extra_data'].get('summary'))
    return jsonify([
        {"text": "Jira ticket created here: {}".format(
            url), "type": 'system_ephemeral', "channel_id": req['channel_id']}
    ])


@app.route("/send-to-other-channel", methods=["POST"])
@csrf.exempt
@check_signature("send-to-other-channel")
@check_enabled("send-to-other-channel")
def send_to_other_channel_action():
    r = request.data
    req = json.loads(r.decode())
    channel_id = req['extra_data']['channel']
    return jsonify([
        {"text": req['text'], "type": '', "channel_id": channel_id},
        {"text": "", "response_type": 'delete'},
        {"text": "Message moved to other channel", "type": 'system_ephemeral'},
    ])


@app.route("/report-abuse", methods=["POST"])
@csrf.exempt
@check_signature("report-abuse")
@check_enabled("report-abuse")
def abuse():
    r = request.data
    req = json.loads(r.decode())
    cfg = config["report-abuse"]
    report_abuse(cfg["webhook_url"], req['text'],
                 "http://localhost:8065", req['team_id'], req['post_id'])
    return jsonify([
        {"text": "Abuse reported", "type": 'system_ephemeral',
            "channel_id": req['channel_id']}
    ])


@app.route("/translate/<lang>", methods=["POST"])
@csrf.exempt
@check_signature("translate")
@check_enabled("translate")
def translate_endpoing(lang):
    r = request.data
    req = json.loads(r.decode())
    cfg = config["translate"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cfg["credentials_file"]
    text = translate(req['text'], lang)
    inplace = request.args.get('inplace', False)

    if inplace:
        return jsonify([
            {"text": text, "response_type": 'edit'}
        ])
    return jsonify([
        {"text": text, "type": 'system_ephemeral'}
    ])


@app.route("/remind-me/<int:seconds>", methods=["POST"])
@csrf.exempt
@check_signature("remind-me")
@check_enabled("remind-me")
def reminder(seconds):
    r = request.data
    req = json.loads(r.decode())

    p = Process(target=remind, args=(get_config("remind-me", "webhook_url"), seconds,
                                     req['username'], req['text'], "http://localhost:8065", req['team_name'], req['post_id']), daemon=True)
    p.start()
    return jsonify([
        {"text": "Reminder set", "type": 'system_ephemeral',
            "channel_id": req['channel_id']}
    ])


@app.route("/autotag", methods=["POST"])
@csrf.exempt
@check_signature("autotag")
@check_enabled("autotag")
def autotag_endpoing():
    r = request.data
    req = json.loads(r.decode())
    tags = autotag(req['text'])
    text = req['text']
    for tag in tags:
        text += " #{}".format(tag[0])
    return jsonify([
        {"text": text, "response_type": 'edit'}
    ])


@app.route("/autocorrect", methods=["POST"])
@csrf.exempt
@check_signature("autocorrect")
@check_enabled("autocorrect")
def autocorrect_endpoing():
    r = request.data
    req = json.loads(r.decode())
    text = autocorrect(req['text'])
    return jsonify([
        {"text": text, "response_type": 'edit'}
    ])


if __name__ == '__main__':
    app.run(host=get_config("main", "host", "0.0.0.0"),
            port=get_config("main", "port", 5000))
