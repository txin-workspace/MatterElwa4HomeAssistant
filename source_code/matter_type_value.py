import json
import copy

import config
import my_log
import chip_clusters_copy

f_matter_devs = open('./MatterJson/allMatterDevices.json', mode='r')
j_matter_devs = json.loads(f_matter_devs.read())
f_matter_devs.close()

# device id: { dev }
config.dict_mdev_name_value = {}
for dev in j_matter_devs['data']:
    type_value = int(dev['deviceId'], 16)
    if type_value in config.device_type_skip_list:
        continue
    
    # cluster id : { clu }
    config.dict_mdev_name_value[type_value] = {}
    for clu in dev['clusters']:
        clu_name = clu['name'].replace('Scenes', 'ScenesManagement').replace(' LAN', 'Lan')\
                            .replace(' on', 'On').replace(' and', 'And').replace(' ', '').replace('/', '')
        if clu_name not in chip_clusters_copy._CLUSTER_NAME_DICT:
            my_log.info(f'not in dict: {clu_name}')
            continue
        
        clu_id = chip_clusters_copy._CLUSTER_NAME_DICT[clu_name]['clusterId']
        clu_info = chip_clusters_copy._CLUSTER_NAME_DICT[clu_name]
        if clu_id in config.cluster_skip_list:
            continue
        
        # attrtube id : {name: '', payload: {} }
        config.dict_mdev_name_value[type_value][clu_id] = {}
        for attr_id, attr_info in clu_info['commands'].items():
            config.dict_mdev_name_value[type_value][clu_id][attr_id] = copy.deepcopy(attr_info)
            

# print(json.dumps(config.dict_mdev_name_value, indent=4))