import ElwaPubClient
import MatterClient
import ConvM2E
import ConvE2M

import time

import my_log
import config

'''
# 
# dict 'device_table' format
# 

# node_id -> int: {
    # endpoint_id -> int: {
        # id -> str: {
            # 'matter_dev_type': int,
            # 'clusters': {
                # id -> int: { attribute_id -> int: value -> any, ...},
            # },
            # 'el_dev_type': str,
            # 'el': {
                # 'desc': {},
                # 'props': { name -> str: value -> any, ...},
            # },
        # },
    # },
# },

'''
device_table = {}


'''
# 
# mid_manange
# 

# mid -> str: {
#    'caching': bool,
#    'time': time.time(),
#    cid -> int: {
#       'node_id': int,
#       'endpoint_id': int,
#       'attrs' : {
#           attr_id -> int: value -> any,
#           ...
#       }
#   }
# }
'''
mid_manange = {}

# clusters format: 
# {
    # {cluster_id -> int: 
        # {attribute_id -> int: value -> any }, 
        # {}, ...
    # }, 
    # {}, ..
# }
def add_device(node_id: int, endpoint_id: int, matter_device_type: int, clusters: list, info_dict: dict):
    # find device_type in el
    if matter_device_type not in config.matter_el_pair:
        my_log.warning(f'[DeviceTable] device type not in eldd, {node_id}-{endpoint_id}: {matter_device_type}')
        return
    
    el_dev_type = config.matter_el_pair[matter_device_type]

    global device_table
    
    check_node_endpoint(node_id, endpoint_id)
    
    # make device id
    dev_id = dev_id_maker(node_id, endpoint_id, el_dev_type)
    
    # check id in table
    if check_dev_exist(node_id, endpoint_id, dev_id) == True:
        my_log.warning(f'[add device] device exist: {node_id}-{endpoint_id}-{matter_device_type}-{dev_id}')
        return
    
    # add device
    el_dev = ConvM2E.dev_conver(el_dev_type, clusters, info_dict, dev_id)
    
    if el_dev == {}: 
        return
    
    device_table[node_id][endpoint_id][dev_id] = {
        'matter_dev_type': matter_device_type,
        'el_dev_type': el_dev_type,
        'el': el_dev, 
        'clusters': clusters
    }
    
    # send to elwa server
    # my_log.debug(f'send to pub lcient {dev_id}|{el_dev}')
    ElwaPubClient.pub_device_delete(dev_id)
    ElwaPubClient.pub_device_create(dev_id, el_dev)
    
        
def delete_node(node_id):
    my_log.info(f'[Device table] delete_node : {node_id}')
    global device_table
    delete_id_list = []
    # find device id -> list
    for eid in device_table[node_id]:
        delete_id_list.extend(list(device_table[node_id][eid]))
    # delete node from table
    delete_id_list.pop(node_id)
    # send device delete message
    for did in delete_id_list:
        ElwaPubClient.pub_device_delete(did)


def value_update(node_id, endpoint_id, cluster_id, attribute_id, new_value, pub_update = True):
    my_log.debug(f'[value_update] {node_id} {endpoint_id} {cluster_id} {attribute_id} {new_value}')
    
    global device_table
    
    # if check_dev_exist(node_id, endpoint_id, ) == False:
    #     my_log.warning(f'[DeviceTable] value_update, device not exist {node_id}-{endpoint_id}-{cluster_id}-{new_value}')
    #     return

    # find device
    dev_id = find_device_by_cluster(node_id, endpoint_id, cluster_id)
    my_log.debug(f'[value_update] found device_id: {dev_id}')
    if dev_id == None:
        my_log.warning(f'[DeviceTable] value_update, cluster not exist {node_id}-{endpoint_id}-{cluster_id}-{new_value}')
        return
    
    # update matter value
    if attribute_id not in device_table[node_id][endpoint_id][dev_id]['clusters'][cluster_id]:
        my_log.debug(f'[value_update] cluster not has this attritube: {cluster_id} - {attribute_id}')
    
    old_val = device_table[node_id][endpoint_id][dev_id]['clusters'][cluster_id][attribute_id]
    device_table[node_id][endpoint_id][dev_id]['clusters'][cluster_id][attribute_id] = new_value
    my_log.debug(f'[value_update] value updated: {node_id}-{endpoint_id}-{cluster_id}-{attribute_id}, old: {old_val}, new: {device_table[node_id][endpoint_id][dev_id]['clusters'][cluster_id][attribute_id]}')
    # update el value
    el_new_pv = ConvM2E.val_conver(
        device_table[node_id][endpoint_id][dev_id]['el_dev_type'],
        {cluster_id: {attribute_id: new_value}},
        device_table[node_id][endpoint_id][dev_id]['clusters'])
    
    my_log.debug(f'[value_update] convered el new pv: {el_new_pv}')
    if el_new_pv != {}:
        device_table[node_id][endpoint_id][dev_id]['el']['props'].update(el_new_pv)
        # send to elwa server
        if pub_update == True:
            for p_name, p_value in el_new_pv.items():
                ElwaPubClient.pub_update(dev_id, p_name, p_value)



def find_device_by_cluster(node_id, endpoint_id, cluster_id):
    global device_table
    
    for dev_id, dev_info in  device_table[node_id][endpoint_id].items():
        if cluster_id not in dev_info['clusters']:
            continue
        return dev_id
    
    return None



def check_node_endpoint(node_id, endpoint_id):
    global device_table
    if node_id not in device_table:
        device_table[node_id] = {}
    if endpoint_id not in device_table[node_id]:
        device_table[node_id][endpoint_id] = {}



def check_dev_exist(node_id, endpoint_id, dev_id):
    global device_table
    if node_id not in device_table:
        return False
    if endpoint_id not in device_table[node_id]:
        return False
    if dev_id not in device_table[node_id][endpoint_id]:
        return False    
    
    return True


def check_dev_exist_by_id(dev_id) -> list:
    global device_table
    for node_id in device_table:
        for endpoint_id in device_table[node_id]:
            if dev_id in device_table[node_id][endpoint_id]:
                return [True, node_id, endpoint_id]
            
    return [False]


def dev_id_maker(node_id, endpoint_id, el_dev_type):
    return f'Matter-{el_dev_type}-{node_id}-{endpoint_id}'


# 
# message status management
# 
def find_mid_by_attr_update(node_id, endpoint_id, cluster_id, attribute_id, new_value):
    global mid_manange
    
    for mid in mid_manange:
        # timeout mid
        if time.time() - mid_manange[mid]['time'] > 3000:
            mid_manange.pop(mid)
            continue
        
        if cluster_id not in mid_manange[mid]:
            continue
        if mid_manange[mid][cluster_id]['node_id'] != node_id:
            continue
        if mid_manange[mid][cluster_id]['endpoint_id'] != endpoint_id:
            continue
        if attribute_id not in mid_manange[mid][cluster_id]['attrs']:
            continue
        if  mid_manange[mid][cluster_id]['attrs'][attribute_id] != new_value:
            continue
        
        return mid
    
    return None


def device_attribute_updated(node_id, endpoint_id, cluster_id, attribute_id, new_value):
    # is operate?
    mid = find_mid_by_attr_update(node_id, endpoint_id, cluster_id, attribute_id, new_value)
    my_log.debug(f'[device_attribute_updated] found mid: {mid}')
    if mid == None:
        # not operate, jsut do update
        value_update(node_id, endpoint_id, cluster_id, attribute_id, new_value)
    else:
        # is operate, manage mid and do other --
        control_result(mid, cluster_id, attr_id=attribute_id)


def device_control(dev_id, el_prop_name, new_value, mid: str, caching: bool):
    my_log.info(f'[device control] {dev_id} {el_prop_name} {new_value} {mid}')
    # check device exist
    dev_check = check_dev_exist_by_id(dev_id)
    my_log.debug(f'[device control] device check -> {dev_check}')
    if dev_check[0] != True:
        ElwaPubClient.pub_result(mid, 404, 'device not exist')
        return
    
    global device_table
    # if new value == now value , send 200
    if device_table[dev_check[1]][dev_check[2]][dev_id]['el']['props'][el_prop_name] == new_value:
        my_log.info(f'[Device control] same value: {dev_id}-{el_prop_name}-{new_value}')
        ElwaPubClient.pub_result(mid, 200)
        return
    
    # conver to matter
    cluster_change = ConvE2M.cmd_conver(
        device_table[dev_check[1]][dev_check[2]][dev_id]['el_dev_type'], 
        el_prop_name, 
        new_value,
        device_table[dev_check[1]][dev_check[2]][dev_id]['clusters'])
    if cluster_change == {}:
        ElwaPubClient.pub_result(mid, 400, 'porperty not writable')
        return
    
    # mid manage
    global mid_manange
    for cid in cluster_change:
        # need for update value
            # node_id, endpoint_id, cluster_id, attribute_id, new_value
        if mid not in mid_manange:
            mid_manange[mid] = {
                'caching': caching,
                'time': time.time(),
            }
            
        mid_manange[mid][cid] = {
            'node_id': dev_check[1],
            'endpoint_id': dev_check[2],
            'attrs' : cluster_change[cid]
        }
        
    # matter client send
    MatterClient.device_control(dev_check[1], dev_check[2], cluster_change, mid)
    
    
def caching_mode_response(mid):
    if mid not in mid_manange:
        my_log.error('[DeviceTable - caching_mode_response] mid not in manage : {}'.format(mid))
        return 
    
    my_log.debug(f'[caching_mode_response] caching == {mid_manange[mid]['caching']}')
    # no caching -> do noting
    if mid_manange[mid]['caching'] == False:
        return
    
    my_log.debug(f'[caching_mode_response] caching == True')
    # caching -> removce mid and pub result
    mid_manange.pop(mid)
    ElwaPubClient.pub_result(mid, 200)
    
    
    
def control_result(mid: str, cid: str, reason = None, attr_id = None):
    global mid_manange
    # splited_midcid = mid_cid.split('#')
    # mid = splited_midcid[0]
    # cid = splited_midcid[1]
    my_log.debug(f'[control_result] {mid}-{cid}-{reason}-{attr_id}-{mid_manange[mid]}')
    
    # check
    if mid not in mid_manange:
        my_log.error('[DeviceTable] mid not in manage : {} {}'.format(mid, cid))
        return 
    if int(cid) not in mid_manange[mid]:
        my_log.error('[DeviceTable] cid not in manage : {} {}'.format(mid, cid))
        return 
    
    # if success, value update 
    if reason == None:
        # all attr 
        # maybe will not use this part
        if attr_id == None:
            for aid in mid_manange[mid][cid]['attrs']:
                value_update(
                    mid_manange[mid][cid]['node_id'], 
                    mid_manange[mid][cid]['endpoint_id'],
                    cid,
                    aid,
                    mid_manange[mid][cid]['attrs'][aid],
                    # pub_update = True
                )
                mid_manange[mid][cid]['attrs'].pop(aid)
        
        # just one attr
        else:
            value_update(
                    mid_manange[mid][cid]['node_id'], 
                    mid_manange[mid][cid]['endpoint_id'],
                    cid,
                    attr_id,
                    mid_manange[mid][cid]['attrs'][attr_id],
                    # pub_update = True
                )
            mid_manange[mid][cid]['attrs'].pop(attr_id)
    
        # if no attr id in cid, remove cid
        if mid_manange[mid][cid]['attrs'] == {}:
            mid_manange[mid].pop(cid)
        
        # if no cid in mid , command success!
        mid_keys = list(mid_manange[mid].keys())
        mid_keys.remove('time')
        mid_keys.remove('caching')
        if mid_keys == []:
            mid_manange.pop(mid)
            ElwaPubClient.pub_result(mid, 200)
    
    # failed
    else:
        # remove item from mid_manage
        mid_manange.pop(mid)
        # send failed message
        ElwaPubClient.pub_result(mid, 500, reason)
        
