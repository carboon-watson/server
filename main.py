import uuid
import base64

from bottle import run, get, post, request
from pydub import AudioSegment

import recognise
import watson


def convert_stream(stream, ext='wav', to='wav', parameters=None):
    binary = base64.b64decode(stream)
    filename = '/tmp/{}.{}'.format(uuid.uuid4(), ext)
    with open(filename, 'wb') as file:
        file.write(binary)
    if to != ext:
        voice = AudioSegment.from_file(filename)
        new_filename = '/tmp/{}.{}'.format(uuid.uuid4(), to)
        voice.export(new_filename, format=to, parameters=parameters)
        return new_filename
    return filename

@post('/auth')
def authtenticate():
    params = request.json.get('params')
    stream = params.get('stream')
    filename = convert_stream(stream, 'm4a', 'wav')
    print(filename)
    result = dict(result=recognise.recognise_voice(filename))
    print(result)
    #recognise.collect('adela', filename)
    return result

@post('/speech/text')
def speech_to_text():
    params = request.json.get('params')
    stream = params.get('stream')
    stream_type = request.json.get('type')
    filename = convert_stream(stream, stream_type, 'flac')
    return watson.speech_to_text(filename, content_type='audio/flac')

@post('/text/speech')
def text_to_speech():
    params = request.json.get('params')
    text = params.get('text')
    filename = watson.text_to_speech(text)
    with open(filename, 'rb') as file:
        return dict(content=base64.b64encode(file.read()))

@post('/text/tone')
def analyze_tone():
    params = request.json.get('params')
    text = params.get('text')
    filename = watson.text_to_speech(text)
    with open(filename, 'rb') as file:
        return dict(content=base64.b64encode(file.read()))


#watson.speech_to_text('/home/abi/Downloads/0001.flac')
#watson.speech_to_text('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', content_type='audio/m4a')
#watson.speech_to_text('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', content_type='audio/m4a')
#print(watson.text_to_speech('Hi Majid, Your balance is 0.2 EUR, you are out of money.'))
#with open('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', 'rb') as f:
#    s = base64.b64encode(f.read())
#    filename = convert_stream(s, ext='m4a', to='wav', parameters='-ar 8000 -ac 1')
#    print(filename)
#    watson.speech_to_text(filename, content_type='audio/flac')

run(host='0.0.0.0', port=8080)
