import my_log
# e2m -> echonet lite to matter
# input el_dev_type -> str, prop_name -> dict, new_value -> any

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
    
controlable_dev = {
    'electricLock',
    'generalLighting',
}

implemented_prop = {
    'operationStatus',
    'lightLevel',
    'mainElectricLock',
    'rgb',
}


def cmd_conver(dev_type, prop_name, new_value, clusters):
    if dev_type not in controlable_dev:
        my_log.warning(f'[cmd_conver] {dev_type} not in controlable_dev')
        return {}
    
    if prop_name not in implemented_prop:
        my_log.warning(f'[cmd_conver] {prop_name} not in implemented_prop')
        return {}
    
    if prop_name == 'operationStatus':
        return prop_operationStatus(new_value)
    elif prop_name == 'lightLevel':
        return prop_lightLevel(new_value, clusters)
    elif prop_name == 'mainElectricLock':
        return prop_mainElectricLock(new_value)
    elif prop_name == 'rgb':
        return prop_rgb(new_value, clusters)
    
    else:
        pass
    
    
def prop_operationStatus(value: bool) -> dict:
    return {6: {0: value}}

def prop_lightLevel(value: int, clusters: dict) -> dict:
    level_min = 0 # default
    level_max = 255 # default
    if 2 in clusters[8]:
        level_min = clusters[8][2]
    if 3 in clusters[8]:
        level_max = clusters[8][3]
        
    level = int(((value / 100) * level_max) + level_min)
        
    return {8: {0: level}}

def prop_mainElectricLock(value: bool) -> dict:
    if value == True:
        return {257: {0: 1}}
    elif value == False:
        return {257: {0: 2}}

def prop_rgb(value: dict, clusters: dict) -> dict:
    # CIE 1931?
    x = int(value['red'] * 0.4124 + value['green'] * 0.3576 + value['blue'] * 0.1805)
    y = int(value['red'] * 0.2126 + value['green'] * 0.7152 + value['blue'] * 0.0722)
    z = int(value['red'] * 0.0193 + value['green'] * 0.1192 + value['blue'] * 0.9505)
    return {
        768: {3: x, 4: y}, 
        8:{0: z}
    }