import json
import copy
import sys

import config
import my_log
import chip_clusters_copy

import MatterClient
import ElwaSubClient
import ElwaPubClient

def cerate_matter_dict():
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


def main(el_addr, el_port, matter_addr, tp_cre, tp_del, tp_upd, tp_ope, tp_res):
    
    my_log.info(f'parameters:\n \
                \tbroker_address: {el_addr}, broker_port: {el_port}\n \
                \tmatter_server_websocket: {matter_addr}')
    
    config.el_mqtt_address = str(el_addr)
    config.el_mqtt_port = int(el_port)
    config.matt_server_address = str(matter_addr)
    
    my_log.info(f'parameters - el server mqtt topic:\n \
        \ttopic_create: {tp_cre}, topic_delete: {tp_del}\n \
        \ttopic_update: {tp_upd}, topic_operate: {tp_ope}\n \
        \ttopic_result: {tp_res}')

    config.el_mqtt_topic_create = str(tp_cre)
    config.el_mqtt_topic_delete = str(tp_del)
    config.el_mqtt_topic_update = str(tp_upd)
    config.el_mqtt_topic_operate = str(tp_ope)
    config.el_mqtt_topic_result = str(tp_res)
    
    cerate_matter_dict()
    MatterClient.matter_client_start()
    ElwaSubClient.sub_start()
    


if __name__ == '__main__':
    if len(sys.argv) != 9:
        sys.exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
    