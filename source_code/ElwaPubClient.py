from paho.mqtt import client as matt_client
import threading
import json
import time

import my_log
import config

    
def pub_device_create(dev_id, dev_el):
    my_log.info(f'[mqtt pub] create {dev_id}')
    mqtt_pub(
        f'{config.el_mqtt_topic_create}/{dev_id}/', 
        {
            'mid': f'{config.mqtt_pub_client_name}_create_{time.time()}',
            'info': {
                'id': dev_id,
                'deviceType': dev_el['desc']['deviceType'],
                'protocol': dev_el['props']['protocol'],
                'manufacturer': dev_el['props']['manufacturer']
            },
            'dd': dev_el['desc'],
            'properties': dev_el['props']
        },
    )


def pub_device_delete(dev_id):
    my_log.info(f'[mqtt pub] delete {dev_id}')
    mqtt_pub(
        f'{config.el_mqtt_topic_delete}/', 
        # f'{config.el_mqtt_topic_delete}/{dev_id}/', 
        {
            'mid': f'{config.mqtt_pub_client_name}_delete_{time.time()}',
            'device_id': dev_id
        },
    )

def pub_update(device_id, prop_name, new_value):
    my_log.debug(f'[pub_update] {device_id}-{prop_name}-{new_value}')
    mqtt_pub_run(
        f'{config.el_mqtt_topic_update}/{device_id}/{prop_name}/', 
        {
            'mid': f'{config.mqtt_pub_client_name}_update_{time.time()}',
            'value': new_value
        }
    )


def pub_result(mid: str, result: int, reason=None):
    my_log.debug(f'[pub_result] {mid}-{result}-{reason}')
    mqtt_pub_run(
        f'{config.el_mqtt_topic_result}/', 
        {
            'mid': mid,
            'result': result,
            'reason': reason
        }
    )





# 
# internel
# 

# pub_client = None

def create_client() -> matt_client.Client:
    # global pub_client
    
    pub_client = matt_client.Client(f'{config.mqtt_pub_client_name}-{time.time()}')
    pub_client.on_connect = on_connect
    pub_client.on_disconnect = on_disconnect
    pub_client.on_publish = on_publish
    
    pub_client.connect(config.el_mqtt_address, config.el_mqtt_port)
    
    return pub_client
    
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        my_log.info('[ElwaPubClient - on_connect] {}-{}-{}-{}'.format(client._client_id, rc, flags, userdata))
    else:
        my_log.error('[ElwaPubClient - on_connect] FAILED! {}-{}-{}-{}'.format(client._client_id, rc, flags, userdata))


def on_disconnect(client: matt_client.Client, userdata, rc):
    my_log.warning('[ElwaPubClient - on_disconnect] {}-{}-{}'.format(client._client_id, userdata, rc))

def on_publish(client: matt_client.Client, userdata, mid):
    my_log.info('[ElwaPubClient - on_publish] {}-{}-{}'.format(client._client_id, mid, userdata))


def mqtt_pub(topic, msg):
    # global pub_client
    client = create_client()
    # pub_client.publish(topic, payload=json.dumps(msg))
    client.publish(topic, payload=json.dumps(msg))
    time.sleep(0.001)
    client.disconnect()
    
def mqtt_pub_run(topic, msg):
    threading.Thread(target = mqtt_pub, args = (topic, msg,)).start()


