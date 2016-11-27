import uuid
import base64
import codecs
import json

from bottle import run, get, post, request
from pydub import AudioSegment

import recognise
import watson

def file_to_base64(filename):
    with open(filename, 'rb') as file:
        return str(base64.b64encode(file.read()))

def file_to_hex(filename):
    with open(filename, 'rb') as file:
        return codecs.encode(file.read(), 'hex').decode()


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
    result = recognise.recognise_voice(filename)
    print(result)
    if result is not None:
        voice_filename = watson.text_to_speech('Hello {}!'.format(result.get('name')))
        result['voice_message'] = file_to_hex(voice_filename)
        return dict(result=result)
    else:
        #recognise.collect('adela', filename)
        voice_filename = watson.text_to_speech('Sorry, I could not recognise you.')
        voice_message = file_to_hex(voice_filename)
        return dict(result=dict(name=None, voice_message=voice_message))

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
    return dict(result=file_to_hex(filename))

@post('/text/tone')
def analyze_tone():
    params = request.json.get('params')
    text = params.get('text')
    filename = watson.text_to_speech(text)
    return dict(result=base64.b64encode(file.read()))

@post('/command/analyse')
def analyse_command():
    params = request.json.get('params')
    stream = params.get('stream')
    intents = params.get('intents')
    context = params.get('context')
    print(context)
    print(intents)
    filename = convert_stream(stream, 'm4a', 'flac')
    print(filename)
    speech_data = watson.speech_to_text(filename, content_type='audio/flac', model='en-US_NarrowbandModel')
    print(json.dumps(speech_data, indent=2))
    text = speech_data['results'][0]['alternatives'][0]['transcript']
    print('text:', text)
    result = watson.conversation(text, context=context)
    print(result)
    return dict(result=result)

#watson.speech_to_text('/home/abi/Downloads/0001.flac')
#watson.speech_to_text('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', content_type='audio/m4a')
#watson.speech_to_text('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', content_type='audio/m4a')
#print(watson.text_to_speech('Hi Majid, Your balance is 0.2 EUR, you are out of money.'))
#with open('/home/abi/Downloads/Telegram Desktop/Start Jet Bank.m4a', 'rb') as f:
#    s = base64.b64encode(f.read())
#    filename = convert_stream(s, ext='m4a', to='wav', parameters='-ar 8000 -ac 1')
#    print(filename)
#    watson.speech_to_text(filename, content_type='audio/flac')

#print(json.dumps(watson.conversation('I want to transfer money.'), indent=2))

run(host='0.0.0.0', port=8080)
