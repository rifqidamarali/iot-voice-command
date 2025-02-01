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

        print('listening wakeword...')
        speech_text = r.recognize_wit(audio, key='PEHSPR7Z3HV25HPJS4UZIPUJAHMP6GIV')
        # check if the wake word is spoken
        if "hello" in speech_text.lower():
            print("Wake word recognized.")
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

def get_text_data(intents, entities, traits):
    if(intents == []):
        intents = 'intent not found'
        intent_confidence = None
    else:
        intent = intents[0]['name']
        intent_confidence = intents[0]['confidence']
    #devices
    if (entities == {}):
        device = 'Device tidak ada'
        device_confidence = 'Kosong'
        velocity = 'Kecepatan tidak ada'
        velocity_confidence = 'tidak ada'

    elif len(list(entities.keys())) >  1:
        device = entities['device:device'][0]['value']
        device_confidence = entities['device:device'][0]['confidence']
        velocity = entities['velocity:velocity'][0]['value']
        velocity_confidence = entities['velocity:velocity'][0]['confidence']

    elif list(entities.keys())[0] == 'device:device':
        device = entities['device:device'][0]['value']
        device_confidence = entities['device:device'][0]['confidence']
        velocity = 'Kecepatan tidak ada'
        velocity_confidence = 'tidak ada'
    
    elif list(entities.keys())[0] == 'velocity:velocity':
        device = 'Kecepatan tidak ada'
        device_confidence = 'tidak ada'
        velocity = entities['velocity:velocity'][0]['value']
        velocity_confidence = entities['velocity:velocity'][0]['confidence']
    # traits
    if(traits == {}):
        value = 'Trait not found'
        value_confidence = 0
    else:
        value = traits['on_off'][0]['value']
        value_confidence = traits['on_off'][0]['confidence']
    print("Text : " + text)
    print("Intent : " + str(intent) + " Confidence : " + str(intent_confidence))
    print("Device : " + str(device) + " Confidence : " + str(device_confidence))
    print("Trait : " + str(value) + " Confidence : " + str(value_confidence))
    print("Velocity : " + str(velocity) + " Confidence : " + str(velocity_confidence))
    result = (intent, device, value)
    return result

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

# create a recognizer

# Define constants for device and value names
while True:
    if recognize_wake_word() is True:
        print("Listening...")
        record_audio()
        resp = None
        msg = speech_recognition()
        if msg is None:
            continue

        else:
            client = Wit('D7L5GGR52R3JFYM3CW5SFZVMMBBQ6COZ') #with trait proto5 
            resp = client.message(msg)
            text = resp['text']
            intents = resp['intents']
            entities = resp['entities']
            traits = resp['traits']
            result = get_text_data(intents, entities, traits)
            handle_device_action(*result)
            break            
            # data = {'Text': text, 'Intent': intent, 'Intent Confidence': intent_confidence, 'Device': device, 'Device Confidence': device_confidence, 'Value': value , 'Trait Confidence': value_confidence, 'Velocity': velocity, 'Velocity Confidence': velocity_confidence}
