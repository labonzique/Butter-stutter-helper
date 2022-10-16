import requests
import constants
import json
from auth import OPENAI_KEY

import openai
openai.api_key = OPENAI_KEY


def get_text(audio_file: bytes) -> str:
    files = [
        ('audio_file', ('filename', audio_file, 'audio/mpeg'))
    ]
    response = requests.request("POST", constants.URL, data={}, files=files)
    return json.loads(response.text)['text']


def get_answer(q: str) -> str:
    completion = openai.Completion.create(
        model='text-davinci-002',
        prompt=q,
        max_tokens=50,
        temperature=0
    )
    return completion.choices[0].text
