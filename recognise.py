from piwho import recognition

MAX_RECOGNISE_RATE = 0.40

rc = recognition.SpeakerRecognizer()

rc.train_new_data('./records/majid-1.wav', 'Majid')
rc.train_new_data('./records/abi-1.wav', 'Abi')

def recognise_voice(filename):
    name = rc.identify_speaker(filename)
    scores = rc.get_speaker_scores()
    best = 1.0
    name = None
    for key in scores:
        rate = float(scores.get(key))
        if rate < best:
            best = rate
            name = key
    if rate > MAX_RECOGNISE_RATE:
        return None
    return dict(name=name, rate=rate)
