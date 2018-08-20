import json
import requests
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import jsonify
from flask_wtf import CSRFProtect

EMOJIS_MAP = {
    0: "joy",
    1: "unamused",
    2: "weary",
    3: "sob",
    4: "heart_eyes",
    5: "pensive",
    6: "ok_hand",
    7: "blush",
    8: "heart",
    9: "smirk",
    10: "grin",
    11: "notes",
    12: "flushed",
    13: "100",
    14: "sleeping",
    15: "relieved",
    16: "relaxed",
    17: "raised_hands",
    18: "two_hearts",
    19: "expressionless",
    20: "sweat_smile",
    21: "pray",
    22: "confused",
    23: "kissing_heart",
    24: "hearts",
    25: "neutral_face",
    26: "information_desk_person",
    27: "disappointed",
    28: "see_no_evil",
    29: "tired_face",
    30: "v",
    31: "sunglasses",
    32: "rage",
    33: "thumbsup",
    34: "cry",
    35: "sleepy",
    36: "stuck_out_tongue_winking_eye",
    37: "triumph",
    38: "raised_hand",
    39: "mask",
    40: "clap",
    41: "eyes",
    42: "gun",
    43: "persevere",
    44: "imp",
    45: "sweat",
    46: "broken_heart",
    47: "blue_heart",
    48: "headphones",
    49: "speak_no_evil",
    50: "wink",
    51: "skull",
    52: "confounded",
    53: "smile",
    54: "stuck_out_tongue_winking_eye",
    55: "angry",
    56: "no_good",
    57: "muscle",
    58: "punch",
    59: "purple_heart",
    60: "sparkling_heart",
    61: "blue_heart",
    62: "grimacing",
    63: "sparkles"
}


def suggest_emoji(text):
    response = requests.get("https://deepmoji.mit.edu/api/", {"q": text})
    data = response.json()
    counter = 0
    maxIdx = None
    for score in data["scores"]:
        if maxIdx is None:
            maxIdx = [counter, score]
        elif maxIdx[1] < score:
            maxIdx = [counter, score]
        counter += 1

    if maxIdx is None:
        return None
    return EMOJIS_MAP[maxIdx[0]]
