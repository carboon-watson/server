import shutil
import uuid
import os, os.path
from piwho import recognition

MAX_RECOGNISE_RATE = 0.40

rc = recognition.SpeakerRecognizer()

rc.train_new_data('./records/majid', 'majid')
rc.train_new_data('./records/abi', 'abi')
rc.train_new_data('./records/adela', 'adela')

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

def collect(id, filename):
    outpath = './records/{}/'.format(id)
    filecount = len([name for name in os.listdir(outpath) if os.path.isfile(os.path.join(outpath, name))]) + 1
    p, e, = filename.split('.')
    shutil.copy(filename, '{}sample-{}.{}'.format(outpath, filecount, e))
