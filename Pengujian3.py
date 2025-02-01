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
def handle_device_action():
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
        else:
            print('kipas angin mati')
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
        print('Try again')
NewDataTest = getRandomValues(LampuKamarRifqiOff, LampuKamarRifqiOn, LampuTerasOff, LampuTerasOn, KipasAnginOff, KipasAnginOn1, KipasAnginOn2, KipasAnginOn3)
# NewDataTest = getRandomValues(KipasAnginOff, KipasAnginOn1, KipasAnginOn2, KipasAnginOn3)
resp = None
client = Wit('PEHSPR7Z3HV25HPJS4UZIPUJAHMP6GIV') #with trait proto6
DataExcel =[]

test = ['kipas angin kecepatan satu', 'nyalakan kipas lampu kecepatan satu dua', 'nyalakan', 'nyalakan kipas']
for x in pengujian:
    # z = client.message(x)
    
    resp = client.message(x)
    text = resp['text']
    print("Text : " + text)
    entity = resp['entities']
    entity_type = []
    for key in entity.keys():
        entity_type.append(key)
    entity_type.sort()
    # print(entity_type)
    entity_value = []
    key_value = []
    entity_confidence =[]
    key_confidence = []
    entity_property ={}
    for i in entity_type:
        entity_value.append(entity[i][0]['value'])
        entity_confidence.append(entity[i][0]['confidence']) #just for test
    entity_property['text'] = text
    for i in range(len(entity_type)):
        key_value.append(entity_type[i])
        key_confidence.append(entity_type[i] + " confidence")
    # handle_device_action()
    # print(key_confidence)
    for i in range(len(entity_type)):    
        entity_property[key_value[i]] = entity_value[i]
        entity_property[key_confidence[i]] = entity_confidence[i]      
    
    print(entity_property)
    data = entity_property
    # new_data = {}
    # for x in entity_value:
    #     if "kipas" in x:
    #         if len(entity_value) == 3:
    #             for key in ['text', 'verb:verb', 'device:device', 'velocity:velocity']:
    #                 new_data[key] = data[key]
    #         elif len(entity_value) < 3:
    #             missing_elements = 3 - len(entity_value)
    #             missing_entit_type = ""
    #             if "verb:verb" not in entity_type:
    #                 missing_entit_type += "verb "
    #                 data['verb:verb'] = ""
    #             if "velocity:velocity" not in entity_type:
    #                 missing_entit_type += "velocity "
    #                 data['velocity:velocity'] = ""
    #             for key in ['text', 'verb:verb', 'device:device', 'velocity:velocity']:
    #                 new_data[key] = data[key]
    #             print(f"Kekurangan: entity_value harus memiliki setidaknya 3 elemen. Kurang {missing_elements} elemen: {missing_entit_type}")
    #     elif "lampu" in x:
    #         if len(entity_value) == 2:
    #             for key in ['text', 'verb:verb', 'device:device']:
    #                 new_data[key] = data[key]
    #         elif len(entity_value) < 2:
    #             missing_entit_type = ""
    #             if "verb:verb" not in entity_type:
    #                 missing_entit_type += "verb "
    #                 data['verb:verb'] = ""
    #                 data['velocity:velocity'] = ""
    #             for key in ['text', 'verb:verb', 'device:device', 'velocity:velocity']:
    #                 new_data[key] = data[key]
    #             print(f"Kekurangan: entity_value harus memiliki setidaknya 2 elemen. Kurang {missing_elements} elemen: {missing_entit_type}")
    #     elif "device:device" not in entity_type:
    #         data['device:device'] = ""
    #         if "verb:verb" not in entity_type:
    #             data['verb:verb'] = ""
    #         if "velocity:velocity" not in entity_type:
    #             data['velocity:velocity'] = ""
    #         for key in ['text', 'verb:verb', 'device:device', 'velocity:velocity']:
    #             new_data[key] = data[key]
    #         print("device not found")
    # data = new_data         
    DataExcel.append(data)
df = pd.DataFrame(DataExcel)
df.to_excel('Pengujian3/DataTest.xlsx', index=False)


# device = ['lampu kamar rifqi','lampu teras', 'kipas angin']
# velocity = ['satu', 'dua', 'tiga']
# verb = ['nyala', 'mati']
