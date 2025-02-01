import pyaudio
import wave
import speech_recognition as sr
from wit import Wit

def recognize_wake_word():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening to wakeword...')
            audio = r.listen(source, phrase_time_limit=2)
        # recognize speech using Google Speech Recognition
        # speech_text = r.recognize_google(audio)
        speech_text = r.recognize_wit(audio, key='PEHSPR7Z3HV25HPJS4UZIPUJAHMP6GIV')
        # check if the wake word is spoken
        if "hello" in speech_text.lower():
            print("Wake word recognized.")
            return True
    except sr.UnknownValueError:
        print("Unable to recognize wakeword.")
        return False
    except sr.RequestError:
        print("Could not request results from Wit.ai service")
        return False

def record_audio():
    filename = 'record.wav'
    duration = 5
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 16000
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    print("Masukkan perintah suara!")
    for i in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Rekaman selesai.")

# create a recognizer
def speech_recognition():
        r = sr.Recognizer()
        with sr.AudioFile('record.wav') as source:
            audio = r.record(source)
        try:
            text = r.recognize_wit(audio, key='PEHSPR7Z3HV25HPJS4UZIPUJAHMP6GIV')
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            # pass
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
# Define constants for device and value names
def get_text_data(entity):
    entity_type = []
    for key in entity.keys():
        entity_type.append(key)
    entity_type.sort()
    entity_value = []
    for i in entity_type:
        entity_value.append(entity[i][0]['value'])
    return entity_value
# Define a function to handle device actions
def handle_device_action(entity_value):
    if "kipas angin" in entity_value:
        if "nyala" in entity_value:
            if "satu" in entity_value:
                print('nyala dengan kecepatan satu')
            elif "dua" in entity_value:
                print('nyala dengan kecepatan dua')
            elif "tiga" in entity_value:
                print('nyala dengan kecepatan tiga')
            else:
                print('kecepatan tidak diketahui')
        elif "mati" in entity_value:
            print('kipas angin mati')
        else:
            print('perintah tidak dikenali')
    elif "lampu kamar rifqi" in entity_value:
        if "nyala" in entity_value:
            print("lampu kamar rifqi nyala")
        else:
            print("lampu kamar rifqi mati")
    elif "lampu teras" in entity_value:
        if "nyala" in entity_value:
            print("lampu kamar teras nyala")
        else:
            print("lampu teras mati")
    else:
        print('perintah tidak dikenali')
while True:
    wake = recognize_wake_word()
    print(wake)
    if wake is True:
        record_audio()
        # resp = None
        msg = speech_recognition()
        if msg is None:
            continue
        else:
            resp = None
            client = Wit('PEHSPR7Z3HV25HPJS4UZIPUJAHMP6GIV')
            resp = client.message(msg)
            text = resp['text']
            entity = resp['entities']
            data = get_text_data(entity)
            handle_device_action(data)
            print(data)
        
        # print("Text : " + text)
        # print("Intent : " + str(intent) + " Confidence : " + str(intent_confidence))
        # print("Device : " + str(device) + " Confidence : " + str(device_confidence))
        # print("State : " + str(value) + " Confidence : " + str(value_confidence))

        # handle_device_action(intent, device, value)