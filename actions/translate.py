# Imports the Google Cloud client library
from google.cloud import translate as trans


def translate(text, target):
    translate_client = trans.Client()
    translation = translate_client.translate(
        text,
        target_language=target)
    return translation['translatedText']
