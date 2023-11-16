from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import ssl
import time
import paho.mqtt.client as mqtt_client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Default value for the variable to store user input
user_input = ""

# MQTT Broker configuration
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
        return ssl_context
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

def publish(client, message):
    msg_count = 1
    while True:
        time.sleep(1)
        result = client.publish(topic, message, 0)
        status = result[0]
        if status == 0:
            print(f"Sent `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 50:
            break

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect()
    subscribe(client)
    client.loop_start()  # Start the MQTT loop in the background

# Define the main route
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user_input": user_input})

# Define a route to handle form submissions
@app.post("/")
async def process_form(request: Request, text_input: str = Form(...)):
    global user_input
    user_input = text_input

    # Publish user input to MQTT broker
    mqtt_client = connect()
    publish(mqtt_client, user_input)
    mqtt_client.disconnect()

    return templates.TemplateResponse("index.html", {"request": request, "user_input": user_input})