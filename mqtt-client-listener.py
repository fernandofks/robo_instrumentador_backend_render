import ssl
import time
import paho.mqtt.client as mqtt_client

broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"
port = 443
topic = "gi/mandando/dados"
client_id = f'aula-6-Giovanni'

ca = "certs/AmazonRootCA1.pem" 
cert = "certs/6f963f6ec45fbc59ebb98cf9df943424944b334aec0a18ce0f2e7f5d256530c9-certificate.pem.crt"
private = "certs/6f963f6ec45fbc59ebb98cf9df943424944b334aec0a18ce0f2e7f5d256530c9-private.pem.key"

def ssl_alpn():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

def connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    ssl_context = ssl_alpn()
    client.tls_set_context(context=ssl_context)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg,0)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 30:
            break
        
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect()
    subscribe(client)
    client.loop_forever()

run()
