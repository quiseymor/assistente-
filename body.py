import queue
import voice
import vosk 
import json
import words
import sounddevice as sd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from skills import *

q = queue.Queue()

model=vosk.Model('model_ru')

device=sd.default.device = 0, 4
samplerate=int(sd.query_devices(device[0], 'input')['default_samplerate'])

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    
    trg = not words.TRIGGERS.intersection(data.split())
    if not words.TRIGGERS.intersection(data.split()):
        return
    
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    func_name = answer.split()[0]

    voice.speaker(answer.replace(func_name, ''))
    exec(func_name + '()')


def main():

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))
    
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))
    del words.data_set

    #постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0], dtype='int16',
                                channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)   

if __name__ == '__main__':
    main()

