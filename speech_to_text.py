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
    instruction: str = 'I am an intelligent question-answering bot that helps people who stutter.' \
                       ' If you ask me a question about stuttering, I will answer.' \
                       ' If you ask me a question that is nonsense, trickery, or irrelevant for stuttering,' \
                       ' I will respond with: "Please ask me about stuttering."'
    prompt: str = f'{instruction}' \
                  f'\n' \
                  f'\nQ: {q}.' \
                  f'\nA: '
    completion = openai.Completion.create(
        model='text-davinci-002',
        prompt=prompt,
        max_tokens=200,
        temperature=0
    )
    return completion.choices[0].text
