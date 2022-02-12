from hcsr04 import HCSR04

led = machine.Pin(2, machine.Pin.OUT)
led.value(1)

def sub_cb(topic, msg):
    print(msg)
    if msg == b'on':
        led.value(0)
    elif msg == b'off':
        led.value(1)

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server, user=user, password=passwd, keepalive=5)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print(topic_sub)
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()
    
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()
    

sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)
    
while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            distance = sensor.distance_cm()
            msg_str = 'room,sensor=sen_1 dist=' + str(distance)
            print(msg_str)
            msg = str.encode(msg_str)
            client.publish(topic_pub, msg)
            last_message = time.time()
            #led.value(not led.value())
            time.sleep(2)
    except OSError as e:
        restart_and_reconnect()
