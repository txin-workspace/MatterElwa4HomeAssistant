import websocket
import threading
import time
import json

import my_log
import config
import DeviceTable

# manange not availabe node
# node_id
node_need_interview = []


matter_client = None

def matter_client_start():
    global matter_client
    matter_client = ws_client()
    # my_log.debug(f'{type(matter_client)}')

class ws_client:
    
    def __init__(self):
        self.ws = websocket.WebSocketApp(
            config.matt_server_address,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)

        # my_log.info('matter client start')
        # self.ws.run_forever()
        
        # if want to run websocket in other thread
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()
        
        conn_timeout = 5
        while not self.ws.sock.connected and conn_timeout:
            time.sleep(0.2)
            conn_timeout -= 0.2

        # self_reconnect()

        # msg_counter = 0
        # while self.ws.sock.connected:
        #     my_log.info('[is connected] {}'.format(msg_counter))
        #     time.sleep(1)
        #     msg_counter += 1
    
    
    def on_message(self, ws, message):
        my_log.info('[on_message] {}'.format(message))
        message_process(json.loads(message))
        
        
    def on_error(self, ws, error):
        my_log.error('[on_error] {}'.format(error))
        
        
    def on_close(self, ws, close_status_code, close_msg):
        my_log.warning('[on_close] ### closed ### {} {}'.format(close_status_code, close_msg))
        
        
    def on_open(self, ws):
        my_log.info('[on_open] connection')
        websocket.enableTrace(False)
        
        self.send_command(
            {
                "message_id": '0', 
                "command": "start_listening"
            }
        )
            
            
    def send_command(self, command):
        my_log.info(f'[send message] {command}')
        self.ws.send(json.dumps(command))
        
        
        
# def client_start_listening():
#     global matter_client
#     matter_client.send_command(
#         {
#             "message_id": '0', 
#             "command": "start_listening"
#         }
#     )
        
        
def device_control(ndoe_id, endpoint_id, cluster_change, msg_id):
    # cluster_id ->  6, 8, 257, 768
    
    for cluster_id in cluster_change:
        command = {
            "message_id": f'{msg_id}#{cluster_id}',
            "command": "device_command",
            "args": {
                "node_id": ndoe_id,
                "endpoint_id": endpoint_id,
                "payload": {},
                "cluster_id": cluster_id,
                "command_name": None,
                "timed_request_timeout_ms": None
            }
        }
        if cluster_id == 6:
            if cluster_change[6][0] == True:
                command['args']['command_name'] = 'On'
            else:
                command['args']['command_name'] = 'Off'
            
        elif cluster_id == 8:
            command['args']['command_name'] = 'MoveToLevel'
            command['args']['payload']['level'] = cluster_change[8][0]
            
        elif cluster_id == 257:
            command['args']['timed_request_timeout_ms'] = 1000
            if cluster_change[257][0] == 1:
                command['args']['command_name'] = 'LockDoor'
            elif cluster_change[257][0] == 2:
                command['args']['command_name'] = 'UnlockDoor'
                
        elif cluster_id == 768:
            command['args']['command_name'] = 'MoveToColor'
            command['args']['payload']['colorX'] = cluster_change[768][3]
            command['args']['payload']['colorY'] = cluster_change[768][4]
        
        else:
            my_log.warning(f'[MatterClient device_control] other cluster type {cluster_id}')
            return
    
    global matter_client
    matter_client.send_command(command)
    
        
def message_process(msg):
    if 'message_id' in msg:
        if msg['message_id'] == '0':
            table_create(msg['result'])
            
        elif msg['message_id'] == '2':
            pass
        
        else:
            # failed result
            if 'error_code' in msg or msg['result'] != None:
                splited_id = msg['message_id'].split('#')
                my_log.error('[Matter Client] device command failed {}'.format(msg))
                if 'result' not in msg:
                    DeviceTable.control_result(splited_id[0], splited_id[1], msg['details'])
                else:
                    DeviceTable.control_result(splited_id[0], splited_id[1], msg['result'])
            
            # true, and caching == true
            else:
                DeviceTable.caching_mode_response(msg['message_id'].split('#')[0])
        
    elif 'event' in msg:
        if msg['event'] == 'attribute_updated':
            value_update(msg['data'])
            
        elif msg['event'] == 'node_updated':
            node_update(msg['data'])
        
        elif msg['event'] == 'node_event':
            # pass
            # just for doorlock 
            # TODO
            return
        
        else:
            my_log.warning(f'[message_process] other type event message, {msg}')
        
    elif 'fabric_id' in msg:
        # TODO ? 
        return
    
    else:
        my_log.warning(f'[message_process] unknow type message, {msg}')
        

# when node changed
def node_update(node_info):
    global node_need_interview
    # node become not available
    if node_info['available'] == False:
        if node_info['node_id'] not in node_need_interview:
            # add to list
            node_need_interview.append(node_info['node_id'])
            # send interview
            global matter_client
            matter_client.send_command(
                {
                    'message_id': '2',
                    'command': 'interview_node',
                    'args': {
                        'node_id': node_info['node_id']
                    }
                }
            )
        # in list
        else:
            node_need_interview.remove(node_info['node_id'])
            # remove from device table
            DeviceTable.delete_node(node_info['node_id'])
    
    # node become available
    else:
        if node_info['node_id'] not in node_need_interview:
            # create node
            table_create([node_info])
        # in list
        else:
            # remove from list
            node_need_interview.remove(node_info['node_id'])
            # no need to do anything, node being normal
        

def table_create(all_info: list):
    for node_info in all_info:
        node_id = node_info['node_id']
        
        my_log.info(f'[table create] node {node_id}')
        
        info_dict = {
            'manufacturer': None,
            'productCode': None,
            'location': None,
            'productionDate': None,
            'serialNumber': None,
            # 'device_id': None,
            'protocol': None
        }
        
        if node_info['available'] != True:
            continue
        
    # 0/ read root node infomation
        # 29/ desctioper
            # /3 part list -->> other endpoint
        my_log.info('[table create] endpoint 0')
        
        endpoint_list = node_info['attributes']['0/29/3']

        # 40/ basic infomation
            # /1 vender name -> manufacturer
        info_dict['manufacturer'] = node_info['attributes']['0/40/1']
            # /2 product id -> productCode
        info_dict['productCode'] = node_info['attributes']['0/40/2']
            # /6 location -> location
        info_dict['location'] = node_info['attributes']['0/40/6']
        
            # if /11 manufacturing date -> productionDate
        if '0/40/11' in node_info['attributes']:
            info_dict['productionDate'] = node_info['attributes']['0/40/11'] 
        
            # if /15 serial-number -> serialNumber  
        if '0/40/15' in node_info['attributes']:
            info_dict['serialNumber'] = node_info['attributes']['0/40/15'] 
        
            # if /18 unique id -> id    
        # if '0/40/18' in node_info['attributes']:
        #     info_dict['device_id'] = node_info['attributes']['0/40/18'] 
        
            # if /21 sprcification versiom -> protocol
        if '0/40/21' in node_info['attributes']:
            info_dict['protocol'] = node_info['attributes']['0/40/21']
            
            
    # endpoints
        for endpoint_id in endpoint_list:
            my_log.info(f'[table create] endpoint {endpoint_id}')
        # /29/ desciptor 
            # /0 device type list
            device_type_list = node_info['attributes'][f'{endpoint_id}/29/0']
            
            # device in this endpoint
            for dt_dict in device_type_list:
                # skip device type that in list
                if dt_dict['0'] in config.device_type_skip_list:
                    continue
                
                my_log.info(f'[table create] device: {dt_dict}')
                
                # '0' : device type (int)
                device_type = dt_dict['0']
                
            # /29/1 serverList 
                my_log.info(f'[table create] {endpoint_id}/29/1')
                cluster_id_list = node_info['attributes'][f'{endpoint_id}/29/1']
                my_log.info(f'[table create] cluster_id_list: {cluster_id_list}')
                # read clusters value
                cluster_list = {}
                # -->> skip 3 29 57
                for cluster_id in cluster_id_list:
                    if cluster_id in config.cluster_skip_list:
                        continue
                    my_log.info(f'[table create] cluster_id:  {cluster_id}')
                    
                    # if two device type in server list
                    if cluster_id not in config.dict_mdev_name_value[device_type]:
                        # cluster id not belone to device type -> skip
                        continue
                    
                    my_log.info(f'[table create] cluster_id not in dict_mdev_name_value[device_type]:  {cluster_id}')
                    
                    cluster_list[cluster_id] = {}
                # /65531 -> attribute list
                    my_log.info(f'[table create] {endpoint_id}/{cluster_id}/65531')
                    attr_list = node_info['attributes'][f'{endpoint_id}/{cluster_id}/65531']
                    for attr_id in attr_list:
                        # 65520 -> 0xfff0
                        if attr_id > 65520:
                            continue
                        
                        # all attribute value which id less than 0xfff0
                        cluster_list[cluster_id][attr_id] = node_info['attributes'][f'{endpoint_id}/{cluster_id}/{attr_id}']
                
                
                # my_log.debug(f'cluster list : {cluster_list}')
                if cluster_list == {}:
                    continue
                
                # send to deviceTable, add device
                DeviceTable.add_device(node_id, endpoint_id, device_type, cluster_list, info_dict)
                
            
# [
    # 18,
    # "1/6/0",
    # false
# ]   
def value_update(msg):
    # node_id = msg[0]
    # new_value = msg[2]
    dev_info = msg[1].split('/')
    # endpoint_id = dev_info[0]
    # cluster_id = dev_info[1]
    # attribute_id = dev_info[2]
    if dev_info[2] != '0':
        my_log.warning(f'[MatterClient] value_update, attribute id not 0: {msg}')
        # return
    
    # DeviceTable.value_update(msg[0], int(dev_info[0]), int(dev_info[1]), int(dev_info[2]), msg[2])
    DeviceTable.device_attribute_updated(msg[0], int(dev_info[0]), int(dev_info[1]), int(dev_info[2]), msg[2])
    