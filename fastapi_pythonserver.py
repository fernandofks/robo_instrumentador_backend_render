import sys
import json
import time
#from PIL import Image
import ssl
import time
import paho.mqtt.client as mqtt_client
#import python-multipart
from fastapi import FastAPI, File, HTTPException, UploadFile, Form

# Initialize FastAPI
app = FastAPI()

broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"
port = 443
topic = "gi/mandando/dados"
client_id = f'Fernando'

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

def publish(client,user_input):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"{user_input}"
        result = client.publish(topic, msg,1)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 30:
            break
        
def run():
    client = connect()
    publish(client)
    client.loop_forever()

# Initialize MQTT
client = connect()

@app.get("/")
async def info():
    return f"Send a POST request to / with an image Will publish results to topic {topic}"
    
@app.post("/")
async def run(image: UploadFile = File(...)):
    try:
        start = time.time()
        
        # Read request data
        contents = "user_input"

        # Do something with the image
        results = ["todo"]
        print('Process took {} seconds'.format(time.time() - start), flush=True)
        
        # Publish to MQTT topic
        print(f'Publish to MQTT {topic}', flush=True)
        (rc, mid) = mqtt_client.publish(topic, json.dumps(results), qos=2)
        print("Code {} while sending message {}: {}".format(rc, mid, mqtt_client.error_string(rc)))
        #if not rc == mqtt.MQTT_ERR_SUCCESS: print("Code {} while sending message {}: {}".format(rc, mid, mqtt.error_string(rc)))

        # Format response
        data = {}
        data['res'] = results
        data['count'] = len(results)
        data['success'] = True
        return data
    except:
        e = sys.exc_info()[1]
        print('Python error with no Exception handler:')
        print('Traceback error: {}'.format(e))
        raise HTTPException(status_code=500, detail=str(e))
    
client.loop_forever()