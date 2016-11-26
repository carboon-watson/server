import uuid
import base64

from bottle import run, get, post, request
from pydub import AudioSegment

import recognise
import watson


def convert_stream(stream, ext='wav', to='wav'):
    binary = base64.b64decode(stream)
    filename = '/tmp/{}.{}'.format(uuid.uuid4(), ext)
    with open(filename, 'wb') as file:
        file.write(binary)
    if to != ext:
        voice = AudioSegment.from_file(filename)
        new_filename = '/tmp/{}.{}'.format(uuid.uuid4(), to)
        voice.export(new_filename, format=to)
        return new_filename
    return filename

@post('/auth')
def authtenticate():
    stream = request.json.get('stream')
    filename = convert_stream(stream)
    return dict(result=recognise.recognise_voice(filename))

@get('/speech/totext')
def speech_to_text():
    stream = request.json.get('stream')
    stream_type = request.json.get('type')
    filename = convert_stream(stream, stream_type, 'flac')
    return watson.speech_to_text(filename, content_type='audio/flac')

@get('/text/tospeech')
def text_to_speech():
    text = request.json.get('text')
    filename = watson.text_to_speech(text)
    with open(filename, 'rb') as file:
        return dict(content=base64.b64encode(file.read()))

@get('/text/tone')
def analyze_tone():
    text = request.json.get('text')
    filename = watson.text_to_speech(text)
    with open(filename, 'rb') as file:
        return dict(content=base64.b64encode(file.read()))


#watson.speech_to_text('/home/abi/Downloads/0001.flac')
#watson.speech_to_text('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', content_type='audio/m4a')
#watson.speech_to_text('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', content_type='audio/m4a')
#print(watson.text_to_speech('Hi Majid, Your balance is 0.2 EUR, you are out of money.'))
#with open('/tmp/8001af39-87e0-4e70-a605-a32a9de79068.wav', 'rb') as f:
#    s = base64.b64encode(f.read())
#    filename = convert_stream(s, ext='wav', to='flac')
#    watson.speech_to_text(filename, content_type='audio/flac')

run(host='0.0.0.0', port=8080)
