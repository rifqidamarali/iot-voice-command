import pyaudio
import wave
import speech_recognition as sr
from scipy import signal
import soundfile as sf
import time
from wit import Wit

def recognize_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        # recognize speech using Google Speech Recognition
        speech_text = r.recognize_google(audio)
        # check if the wake word is spoken
        if "hello" in speech_text.lower():
            return True
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print("Could not request results from Wit.ai service")
    return False

def speech_recognition():
        r = sr.Recognizer()
        with sr.AudioFile('record.wav') as source:
            # r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            try:
                # text = r.recognize_google(audio, language="id-ID")
                text = r.recognize_wit(audio, key='JCDWDCW2IR244SXQITIEJ4XTGMGLJ7UW')
                print("You said: " + text)
                return text
                
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                # recognize_wake_word()
                return None
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

def record_audio():
    # konfigurasi audio
    filename = 'record.wav'
    duration = 5
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 16000

    # inisialisasi PyAudio
    p = pyaudio.PyAudio()

    # membuka stream audio
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    # membuat buffer untuk merekam audio
    frames = []
    print("Masukkan perintah suara!")
    # merekam audio selama durasi tertentu
    for i in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    # menutup stream audio
    stream.stop_stream()
    stream.close()

    # menutup PyAudio
    p.terminate()

    # menyimpan hasil rekaman audio dalam file WAV
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Rekaman selesai.")

# create a recognizer

# Define constants for device and value names

# Define a function to handle device actions
def handle_device_action(intent, device, value):
    if intent == 'controlLamp':
        if device == 'lampu kamar rifqi':
            if value == '1':
                print('lampu kamar rifqi nyala')
                # GPIO.output(lamp1, True)
            elif value == '0':
                print('lampu kamar rifqi mati')
                # GPIO.output(lamp1, False)
        elif device == 'lampu teras':
            if value == '1':
                print('lampu kamar teras nyala')
                # GPIO.output(lamp2, True)
            elif value == '0':
                print('lampu kamar teras mati')
                # GPIO.output(lamp2, False)
    elif intent == 'controlFan': 
        if device == 'kipas angin':
            if value == '0':
                print('kipas angin mati')
                # GPIO.output(lamp2, False)
            elif value == '1':
                print('kipas angin nyala dengan lambat')
                # GPIO.output(lamp2, False)
            elif value == '2':
                print('kipas angin nyala dengan sedang')
                # GPIO.output(lamp2, False)
            elif value == '3':
                print('kipas angin nyala dengan sedang')
    else:
        print('Try again')

while True:
    if recognize_wake_word():
        print("Wake word recognized. Listening...")
        record_audio()
        resp = None
        msg = speech_recognition()
        if msg is None:
            continue

        else:
        
            client = Wit('JCDWDCW2IR244SXQITIEJ4XTGMGLJ7UW')
            # with open('record.wav', 'rb') as f:
            #     resp = client.speech(f, {'Content-Type': 'audio/wav'})
            resp = client.message(msg)
            # resp = client.message('nyalakan lampu')
            # res = json.loads(resp)
            # res.keys()
            #text
            text = resp['text']
            intents = resp['intents']
            entities = resp['entities']
            traits = resp['traits']
            #Intents
            if(intents == []):
                intent = 'intent not found'
                intent_confidence = None
            else:
                intent = intents[0]['name']
                intent_confidence = intents[0]['confidence']
            #devices
            if (entities == {}):
                device = 'Device not found'
                device_confidence = 'Kosong'
            elif list(entities.keys())[0] == 'device:lamp':
                device = entities['device:lamp'][0]['value']
                device_confidence = entities['device:lamp'][0]['confidence']
            elif list(entities.keys())[0] == 'device:fan':
                device = entities['device:fan'][0]['value']
                device_confidence = entities['device:fan'][0]['confidence']
            #traits
            if(traits == {}):
                value = 'Trait not found'
                value_confidence = None
            elif (list(traits.keys())[0] == 'TLamp') :
                value = traits['TLamp'][0]['value']
                value_confidence = traits['TLamp'][0]['confidence']
            elif(list(traits.keys())[0] == 'TFan' ):
                value = traits['TFan'][0]['value']
                value_confidence = traits['TFan'][0]['confidence']
            else:
                value = 'Tidak ada trait'
                value_confidence = 'kosong'
            # print(resp)
            # print(resp['traits'])
            print("Text : " + text)
            print("Intent : " + str(intent) + " Confidence : " + str(intent_confidence))
            print("Device : " + str(device) + " Confidence : " + str(device_confidence))
            print("State : " + str(value) + " Confidence : " + str(value_confidence))

            handle_device_action(intent, device, value)
            break