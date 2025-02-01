from wit import Wit
import random
import pandas as pd
import openpyxl

from data.LampuKamarRifqiOn import LampuKamarRifqiOn
from data.LampuKamarRifqiOff import LampuKamarRifqiOff
from data.LampuTerasOn import LampuTerasOn
from data.LampuTerasOff import LampuTerasOff
from data.KipasAnginOff import KipasAnginOff
from data.KipasAnginOn1 import KipasAnginOn1
from data.KipasAnginOn2 import KipasAnginOn2
from data.KipasAnginOn3 import KipasAnginOn3
from data.Test import pengujian

def getRandomValues(*args):
    DataTest = []
    for arr in args:
        random_values = random.sample(arr, 10)
        DataTest.extend(random_values)
    return DataTest

NewDataTest = getRandomValues(LampuKamarRifqiOff, LampuKamarRifqiOn, LampuTerasOff, LampuTerasOn, KipasAnginOff, KipasAnginOn1, KipasAnginOn2, KipasAnginOn3)
# NewDataTest = getRandomValues(KipasAnginOff, KipasAnginOn1, KipasAnginOn2, KipasAnginOn3)
resp = None
client = Wit('D7L5GGR52R3JFYM3CW5SFZVMMBBQ6COZ') #with trait proto5
DataExcel =[]

for x in pengujian:
    # z = client.message(x)
    resp = client.message(x)
    text = resp['text']
    #Intents
    if(resp['intents'] == []):
        intent = 'unidentified'
        intent_confidence = 0
    else:
        intent = resp['intents'][0]['name']
        intent_confidence = resp['intents'][0]['confidence']
    #devices
    if (resp['entities'] == {}):
        device = 'unidentified'
        device_confidence = 0
        velocity = 'unidentified'
        velocity_confidence = 0

    elif len(list(resp['entities'].keys())) >  1:
        device = resp['entities']['device:device'][0]['value']
        device_confidence = resp['entities']['device:device'][0]['confidence']
        velocity = resp['entities']['velocity:velocity'][0]['value']
        velocity_confidence = resp['entities']['velocity:velocity'][0]['confidence']

    elif list(resp['entities'].keys())[0] == 'device:device':
        device = resp['entities']['device:device'][0]['value']
        device_confidence = resp['entities']['device:device'][0]['confidence']
        velocity = 'Kecepatan tidak ada'
        velocity_confidence = 'tidak ada'
    
    elif list(resp['entities'].keys())[0] == 'velocity:velocity':
        device = 'Kecepatan tidak ada'
        device_confidence = 'tidak ada'
        velocity = resp['entities']['velocity:velocity'][0]['value']
        velocity_confidence = resp['entities']['velocity:velocity'][0]['confidence']
    # traits
    if(resp['traits'] == {}):
        value = 'unidentified'
        value_confidence = 0
    else:
        value = resp['traits']['on_off'][0]['value']
        value_confidence = resp['traits']['on_off'][0]['confidence']
    # print(resp)
    # print(resp['traits'])
    print("Text : " + text)
    print("Intent : " + str(intent) + " Confidence : " + str(intent_confidence))
    print("Device : " + str(device) + " Confidence : " + str(device_confidence))
    print("Trait : " + str(value) + " Confidence : " + str(value_confidence))
    print("Velocity : " + str(velocity) + " Confidence : " + str(velocity_confidence))
    data = {'Text': text, 'Intent': intent, 'Intent Confidence': intent_confidence, 'Device': device, 'Device Confidence': device_confidence, 'Value': value , 'Trait Confidence': value_confidence, 'Velocity': velocity, 'Velocity Confidence': velocity_confidence}
    DataExcel.append(data)

df = pd.DataFrame(DataExcel)
df.to_excel('Pengujian2/DataTest.xlsx', index=False)
