from wit import Wit
import random
import pandas as pd

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
resp = None
client = Wit('JCDWDCW2IR244SXQITIEJ4XTGMGLJ7UW') #with trait proto3
# # client = Wit('22NBRT6GPYT7UFIOMNTEXSVJVS364NXV')
DataExcel =[]

for x in pengujian:
    # z = client.message(x)
    resp = client.message(x)
    text = resp['text']
    #Intents
    if(resp['intents'] == []):
        intent = 'intent not found'
        intent_confidence = None
    else:
        intent = resp['intents'][0]['name']
        intent_confidence = resp['intents'][0]['confidence']
    #devices
    if (resp['entities'] == {}):
        device = 'Device not found'
        device_confidence = 'Kosong'
    elif list(resp['entities'].keys())[0] == 'device:lamp':
        device = resp['entities']['device:lamp'][0]['value']
        device_confidence = resp['entities']['device:lamp'][0]['confidence']
    elif list(resp['entities'].keys())[0] == 'device:fan':
        device = resp['entities']['device:fan'][0]['value']
        device_confidence = resp['entities']['device:fan'][0]['confidence']
    # traits
    if(resp['traits'] == {}):
        value = 'Trait not found'
        value_confidence = 0
    elif (list(resp['traits'].keys())[0] == 'TLamp') :
        name = 'TLamp'
        value = resp['traits']['TLamp'][0]['value']
        value_confidence = resp['traits']['TLamp'][0]['confidence']
    elif(list(resp['traits'].keys())[0] == 'TFan' ):
        name = 'TFan'
        value = resp['traits']['TFan'][0]['value']
        value_confidence = resp['traits']['TFan'][0]['confidence']
    # print(resp)
    # print(resp['traits'])
    print("Text : " + text)
    print("Intent : " + str(intent) + " Confidence : " + str(intent_confidence))
    print("Device : " + str(device) + " Confidence : " + str(device_confidence))
    print("Trait : " + str(value) + " Confidence : " + str(value_confidence))
    data = {'Text': text, 'Intent': intent, 'Intent Confidence': intent_confidence, 'Device': device, 'Device Confidence': device_confidence,'Trait': name,  'Value': value , 'Trait Confidence': value_confidence}
    DataExcel.append(data)

df = pd.DataFrame(DataExcel)
df.to_excel('Pengujian1/DataTest.xlsx', index=False)
# resp = None
# # print(LampuKamarRifqiOn)
# client = Wit('JCDWDCW2IR244SXQITIEJ4XTGMGLJ7UW') #with trait
# # # client = Wit('22NBRT6GPYT7UFIOMNTEXSVJVS364NXV')
