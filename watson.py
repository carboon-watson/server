import uuid
import json

from watson_developer_cloud import SpeechToTextV1, TextToSpeechV1, ToneAnalyzerV3, ConversationV1

def speech_to_text(filename, content_type='audio/wav', model='en-US_NarrowbandModel'):
    speech_to_text = SpeechToTextV1(
        username='0ca0d966-fa1d-4d11-90bc-568ce6517f78',
        password='PotZm5sue2tu',
        x_watson_learning_opt_out=False
    )
    #print(json.dumps(speech_to_text.models(), indent=2))
    #print(json.dumps(speech_to_text.get_model('en-US_NarrowbandModel'), indent=2))
    with open(filename, 'rb') as audio_file:
        result = speech_to_text.recognize(
            audio_file, model=model, content_type=content_type, timestamps=True, word_confidence=True)
        print(json.dumps(result, indent=2))
        return result

def text_to_speech(text):
    text_to_speech = TextToSpeechV1(
        username='e45245de-a3b2-4198-b233-96e9f46eb8b0',
        password='XPpKgmuH2v5Q',
        x_watson_learning_opt_out=True)  # Optional flag
    #print(json.dumps(text_to_speech.voices(), indent=2))
    filename = '/tmp/{}.flac'.format(uuid.uuid4())
    with open(filename, 'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(text, accept='audio/flac', voice="en-US_LisaVoice"))
    result = text_to_speech.pronunciation('Watson', pronunciation_format='spr')
    return filename

def analyze_tone(text):
    tone_analyzer = ToneAnalyzerV3(
    username='',
    password='YOUR SERVICE PASSWORD',
    version='2016-02-11')

    print(json.dumps(tone_analyzer.tone(text='I am very happy'), indent=2))

def conversation(text, intents=None, context=None):
    conversation = ConversationV1(
        username='27b4623e-47e1-48b1-be9d-9c0a47c33fc5',
        password='fZEQ1RwGopbU',
        version='2016-09-20')

    # replace with your own workspace_id
    workspace_id = '0b6a2a5f-b6c7-4a60-8d98-2cb075548139'

    response = \
        conversation.message(workspace_id=workspace_id,
            message_input={'text': text},
            intents=intents,
            context=context)
    return response
