import requests
import constants
import json


# def get_text(audio_filepath: str) -> str:
#     files = [
#         ('audio_file', ('filename', open(audio_filepath, 'rb'), 'audio/mpeg'))
#     ]
def get_text(audio_file: bytes) -> str:
    files = [
        ('audio_file', ('filename', audio_file, 'audio/mpeg'))
    ]
    response = requests.request("POST", constants.URL, data={}, files=files)
    return json.loads(response.text)['text']
