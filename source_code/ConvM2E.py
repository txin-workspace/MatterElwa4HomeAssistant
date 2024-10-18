import math
import json

import my_log

# m2e -> matter to echonet lite
# input el_dev_type -> str, clusters -> dict

# implemented
    # electricLock
    # openCloseSensor
    # generalLighting
    # humanDetectionSensor
    # humiditySensor
    # temperatureSensor

# not yet
    # illuminanceSensor
    # controller
    # airCleaner
    # refrigerator
    # homeAirConditioner
    # washerDryer
    # switch
    # waterFlowMeter

# 
# output
# 
# {
    # 'desc': {},
    # 'props': { name -> str: value -> any , ...},
# },

implemented = [
    'electricLock',
    'openCloseSensor',
    'generalLighting',
    'humanDetectionSensor',
    'humiditySensor',
    'temperatureSensor',
]

def check_dev_type_implement(dev_type):
    global implemented
    if dev_type not in implemented:
        my_log.warning(f'[ConvM2E] check_dev_type_implement not implemented yet {dev_type}')
        return False
    return True

# clusters format: 
# {
    # {cluster_id -> int: 
        # {attribute_id -> int: value -> any }, 
        # {}, ...
    # }, 
    # {}, ..
# }
def dev_conver(dev_type: str, clusters: dict, info_dict: dict, dev_id: str) -> dict:
    # my_log.debug(f'|{dev_type}|{clusters}|{info_dict}|{dev_id}|')
    
    if check_dev_type_implement(dev_type) == False:
        return {}
    
    el_props = cluster_conv(clusters)
    el_props.update(info_prop_conv(info_dict))
    el_props.update({'id': dev_id})
    el_desc = desc_maker(dev_type, el_props)
    
    return {'desc': el_desc, 'props': el_props}



def val_conver(dev_type: str, clusters: dict, cluster_ref: dict) -> dict:
    if check_dev_type_implement(dev_type) == False:
        return {}
    
    el_props = cluster_conv(clusters, cluster_ref)
    
    return el_props
    


def desc_maker(dev_type: str, el_props: dict) -> dict:
    dev_desc = {}
    with open(f'./EchonetLiteDD/{dev_type}.json') as f_dev:
        dev_desc.update(json.loads(f_dev.read()))
    with open('./EchonetLiteDD/commonItems.json') as f_comm:
        dev_desc['properties'].update(json.loads(f_comm.read())['properties'])
        
    # TODO
    # delete props not exist
    
    return dev_desc


# info_dict = {
#     'manufacturer': None,
#     'productCode': None,
#     'location': None,
#     'productionDate': None,
#     'serialNumber': None,
#     # 'device_id': None,
#     'protocol': None
# }
def info_prop_conv(info_dict: dict) -> dict:
    return {
        'manufacturer': {
            'code': 'Matter-Device',
            'descriptions': {
                'ja': info_dict['manufacturer'],
                'en': info_dict['manufacturer']
            }
        },
        'productCode' : info_dict['productCode'],
        'location': info_dict['location'],
        'productionDate': info_dict['productionDate'],
        'serialNumber': info_dict['serialNumber'],
        'protocol': {
            'type': 'Matter',
            'version': info_dict['protocol']
        }
    }


def cluster_conv(clusters: dict, cluster_ref = None) -> dict:
    if cluster_ref == None:
        cluster_ref = clusters
        
    el_props = {}
        
    for cluster_id in clusters:
        if cluster_id == 6:
            my_log.debug('[cluster_conv] 6 cluster_OnOff')
            if 0 not in clusters[cluster_id]:
                my_log.debug('[cluster_conv] skip') 
                continue
            el_props.update(cluster_OnOff(clusters[cluster_id]))
            
        elif cluster_id == 8:
            my_log.debug('[cluster_conv] 8 cluster_LevelControl')
            if 0 not in clusters[cluster_id]: 
                my_log.debug('[cluster_conv] skip')
                continue
            el_props.update(cluster_LevelControl(clusters[cluster_id]))
            
        elif cluster_id == 69:
            my_log.debug('[cluster_conv] 69 cluster_BooleanState')
            if 0 not in clusters[cluster_id]: 
                my_log.debug('[cluster_conv] skip')
                continue
            el_props.update(cluster_BooleanState(clusters[cluster_id]))
            
        elif cluster_id == 257:
            my_log.debug('[cluster_conv] 257 cluster_DoorLock')
            if 0 not in clusters[cluster_id]: 
                my_log.debug('[cluster_conv] skip')
                continue
            el_props.update(cluster_DoorLock(clusters[cluster_id]))
            
        elif cluster_id == 768:
            my_log.debug(f'[cluster_conv] 768 cluster_ColorControl {clusters} {cluster_ref}')
            c_dict = {}
            
            if 8 not in cluster_ref: 
                my_log.debug('[cluster_conv] 8 skip')
                continue
            if 3 not in clusters[cluster_id]: c_dict[3] = cluster_ref[768][3]
            else: c_dict[3] = clusters[768][3]
            if 4 not in clusters[cluster_id]: c_dict[4] = cluster_ref[768][4]
            else: c_dict[4] = clusters[768][4]
                
            el_props.update(cluster_ColorControl(c_dict, cluster_ref[8]))
            
        # elif cluster_id == 1024:
            # el_props.update(cluster_IlluminaceMeasurement(clusters[cluster_id]))
            
        elif cluster_id == 1026:
            my_log.debug('[cluster_conv] 1026 cluster_TemperatureMeasurement')
            if 0 not in clusters[cluster_id]: 
                my_log.debug('[cluster_conv] skip')
                continue
            el_props.update(cluster_TemperatureMeasurement(clusters[cluster_id]))
            
        elif cluster_id == 1029:
            my_log.debug('[cluster_conv] 1029 cluster_RelativeHumidityMeasurement')
            if 0 not in clusters[cluster_id]: 
                my_log.debug('[cluster_conv] skip')
                continue
            el_props.update(cluster_RelativeHumidityMeasurement(clusters[cluster_id]))
            
        elif cluster_id == 1030:
            my_log.debug('[cluster_conv] 1030 cluster_OccupancySensing')
            if 0 not in clusters[cluster_id]: 
                my_log.debug('[cluster_conv] skip')
                continue
            el_props.update(cluster_OccupancySensing(clusters[cluster_id]))
            
        else:
            my_log.warning(f'[ConvM2E] cluster_conv not implemented yet {cluster_id}')
            
    return el_props


# 
def cluster_OnOff(cluster_6_dict: dict) -> dict: 
    # 0: 'operationStatus', 
    return {'operationStatus': cluster_6_dict[0]}


level_last = 0
def cluster_LevelControl(cluster_8_dict: dict) -> dict:
    global level_last
    
    my_log.debug(f'[cluster_LevelControl] {cluster_8_dict}')
    # 0: 'lightLevel',
    # 3: 'lightLevelStep',
    level_min = 0 # default
    level_max = 255 # default
    if 2 in cluster_8_dict:
        level_min = cluster_8_dict[2]
    if 3 in cluster_8_dict:
        level_max = cluster_8_dict[3]
        
    level = int(((cluster_8_dict[0] - level_min) / level_max) * 100)
    if level == level_last:
        return {}
    level_last = level
    # TODO
    # if dev_type == light : lightlevel
    # else: 
    return {'lightLevel': level}



def cluster_BooleanState(cluster_69_dict: dict) -> dict:
    # 0: 'openingDetectionStatus2', 
    if cluster_69_dict[0] == 0:
        return {'openingDetectionStatus2': False}
    return {'openingDetectionStatus2': True}



def cluster_DoorLock(cluster_257_dict: dict) -> dict:
    # 0: 'mainElectricLock'
    if cluster_257_dict[0] == 1:
        return {'mainElectricLock': True}
    elif cluster_257_dict[0] == 2:
        return {'mainElectricLock': False}
    


def cluster_ColorControl(cluster_768_dict: dict, cluster_8_dict: dict) -> dict:
    # my_log.debug(f'[cluster_ColorControl] {cluster_768_dict} {cluster_8_dict}')
    # hsv?hsl? -> rgb
    # 768
        # 0 current hue -> option max 254 0xfe
        # 1 current saturation -> option max 254 0xfe
        # ?
        # 3 current X -> mandatory max 65279 0xfeff
        # 4 current Y -> mandatory max 65279 0xfeff
    # 8
        # 0 current level -> default null -> if null -> min level -> if none -> 0
        # 2 min level -> max 254
        # 3 max level -> max 254
    
    # xyz -> rgb
    # CIE 1931?
    # sRGB? 
    x = cluster_768_dict[3] / 65279
    y = cluster_768_dict[4] / 65279
    max_level = 254
    if 3 in cluster_8_dict: 
        max_level = cluster_8_dict[3]
    z = cluster_8_dict[0] / max_level
    
    r = x *  3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y *  1.8760108 + z *  0.0415560
    b = x *  0.0556434 + y * -0.2040259 + z *  1.0572252
    
    # if r > 0.0031308:  
    #     r = 1.055 * math.pow(r, 1 / 2.4) - 0.055
    # else: 
    #     r = (12.92 * r) * 255.0
        
    # if g > 0.0031308: 
    #     g = 1.055 * math.pow(g, 1 / 2.4) - 0.055
    # else: 
    #     g = (12.92 * g) * 255.0
        
    # if b > 0.0031308: 
    #     b = 1.055 * math.pow(b, 1 / 2.4) - 0.055
    # else: 
    #     b = (12.92 * b) * 255.0
    
    return {
        'rgb': 
            {
                # 'red': int(r * 255), 
                # 'green': int(g * 255), 
                # 'blue': int(b * 255), 
                'red': int(abs(r) * 255), 
                'green': int(abs(g) * 255), 
                'blue': int(abs(b) * 255), 
            }
        }
    


def cluster_IlluminaceMeasurement(cluster_1024_dict: dict) -> dict:
    # 0: 'valueInLux',
    return {'valueInLux': cluster_1024_dict[0]}



def cluster_TemperatureMeasurement(cluster_1026_dict: dict) -> dict:
    # 0: 'value',
    if cluster_1026_dict[0] != None:
        return {'value': cluster_1026_dict[0] / 100}



def cluster_RelativeHumidityMeasurement(cluster_1029_dict: dict) -> dict:
    # 0: 'value',
    if cluster_1029_dict[0] != None:
        return {'value': cluster_1029_dict[0] / 100}



def cluster_OccupancySensing(cluster_1030_dict: dict) -> dict:
    # 0: 'detection',
    if cluster_1030_dict[0] == 0:
        return {'detection': False}
    else:
        return {'detection': True}