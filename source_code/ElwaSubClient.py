from paho.mqtt import client as mqtt_client
import json
import threading

import my_log
import config
import DeviceTable
    

def sub_start():
    sub_client = mqtt_client.Client(config.mqtt_sub_client_name)
    sub_client.on_connect = on_connect
    sub_client.on_disconnect = on_disconnect
    sub_client.on_message = on_message
    sub_client.on_subscribe = on_subscribe
    
    sub_client.connect(config.el_mqtt_address, config.el_mqtt_port)
    # sub_client.loop_start()
    sub_client.loop_forever()
    # my_log.info('mqtt sub client started')
    
    
def on_connect(client: mqtt_client.Client, userdata, flags, rc):
    if rc == 0:
        my_log.info('[ElwaPubClient - on_connect] {}-{}-{}-{}'.format(client._client_id, rc, flags, userdata))
        client.subscribe(f'{config.el_mqtt_topic_operate}/#')
    else:
        my_log.error('[ElwaPubClient - on_connect] FAILED! {}-{}-{}-{}'.format(client._client_id, rc, flags, userdata))


def on_disconnect(client, userdata, rc):
    my_log.error('[ElwaSubClient - on_disconnect] user_data: {}, rc: {}'.format(userdata, rc))


def on_subscribe(client, userdata, mid, granted_qos):
    my_log.info('[ElwaSubClient - on_subscribe] {}-{}-{}-{}'.format(client._client_id, userdata, mid, granted_qos))
    

def on_message(client, userdata, msg):
    my_log.info('[ElwaSubClient - on_message] message: {} {}'.format(msg.topic, msg.payload))
    
    splited_topic = msg.topic.split('/')
    if '' in splited_topic:
        splited_topic.remove('')
    pld_json = json.loads(msg.payload)
    
    # dev_id = splited_topic[1]
    # prop_name = splited_topic[2]
    # new_value = pld_json['value']
    # mid = pld_json['mid']
    
    DeviceTable.device_control(splited_topic[-2], splited_topic[-1], pld_json['value'], pld_json['mid'], pld_json['caching'])
    
    
