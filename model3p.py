import pvporcupine as p
import pyaudio
import speech_recognition as sr
import struct
import wave
import os
import time
from mutagen.mp3 import MP3
from wit import Wit
led1 = 23
led2 = 24

def get_file_duration(audio_file):
    audio = MP3(audio_file)
    duration = audio.info.length
    return duration

def play(audio_file):
    os.system(audio_file)
    wait_for = get_file_duration(audio_file)
    time.sleep(wait_for)

def recognize_wake_word():
    porcupine = None
    pa = None
    audio_stream = None

    play('sound\WakeWord.wav')
    print('listening to wakeword...')
    
    # print(p.KEYWORDS)
    # {'grasshopper', 'ok google', 'americano', 'hey barista', 'terminator', 'bumblebee', 'picovoice', 'blueberry', 'grapefruit', 'computer', 'hey google', 'hey siri', 'alexa', 'jarvis', 'porcupine', 'pico clock'}

    try:
        porcupine = p.create(access_key='voEsNGuxtLgSMyZ6kqtMnr7F3OgGJKsqw+9frnPUFY+ZLaQCUrKPKA==',
                             keywords = ["picovoice"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate= porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        # print(porcupine.frame_length, porcupine.sample_rate)

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            # print(f'keyword index {keyword_index}')
            if keyword_index >= 0:
                # print('wakeword detected')
                # print(f'keyword index {keyword_index}')
                # return keyword_index 
                return True
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
    
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
    play('sound\Speak.wav')
    print('Masukkan perintah suara')
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
def speech_recognition():
    r = sr.Recognizer()
    with sr.AudioFile('record.wav') as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        try:
            # text = r.recognize_google(audio, language="id-ID")
            text = r.recognize_wit(audio, key='PEHSPR7Z3HV25HPJS4UZIPUJAHMP6GIV')
            text = text.lower()
            print("You said: " + text)
            return text
        except sr.UnknownValueError as e:
            print("Sistem tidak dapat mentranskripsi perintah suara")
            play("sound\\UnknownValueError.wav")
            pass
        except sr.RequestError as e:
            print("mohon periksa koneksi internet pada sistem")
            play("sound\RequestError.wav")
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
                play('sound\KA1.wav')
            elif "dua" in entity_value:
                print('nyala dengan kecepatan dua')
                play('sound\KA2.wav')
            elif "tiga" in entity_value:
                print('nyala dengan kecepatan tiga')
                play('sound\KA3.wav')
            else:
                print('kecepatan tidak diketahui')
                play('sound\VelocityUnknown.wav')
        elif "mati" in entity_value:
            print('kipas angin mati')
            play('sound\KA0.wav')
        else:
            print('perintah tidak dikenali')
            play('sound\TryAgain.wav')
    elif "lampu kamar rifqi" in entity_value:
        if "nyala" in entity_value:
            # GPIO.output(led1, True)
            print("lampu kamar rifqi nyala")
            play('sound\LKR1.wav')
        elif "mati" in entity_value:
            # GPIO.output(led1, False)
            print("lampu kamar rifqi mati")
            play('sound\LKR0.wav')
        else:
            print('perintah tidak dikenali')
            play('sound\TryAgain.wav')
    elif "lampu teras" in entity_value:
        if "nyala" in entity_value:
            # GPIO.output(led1, True)
            print("lampu kamar teras nyala")
            play('sound\LT1.wav')
        elif "mati" in entity_value:
            # GPIO.output(led1, False)
            print("lampu teras mati")
            play('sound\LT0.wav')
        else:
            print('perintah tidak dikenali')
            play('sound\TryAgain.wav')
    else:
        print('Try again')
        play('sound\TryAgain.wav')

while True:
    wake = recognize_wake_word()
    print(wake)
    if recognize_wake_word:
        record_audio()
        # resp = None
        msg = speech_recognition()
        print(msg)
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