from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import HTMLResponse
import ssl
import time
import paho.mqtt.client as mqtt_client
import crud, models, schemas
from database import SessionLocal, engine
import json
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    time.sleep(1)
    result = client.publish(topic, message, 0)
    status = result[0]
    if status == 0:
        print(f"Sent `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/e/")
async def process_form(request: Request):
    #created_kit = crud.create_kit(db=db, kit=kit)
    #order = crud.get_order(db, created_kit.order_id)
    #order_items = order.items
    
    try:
        argumento_envio = await request.json()
        print(argumento_envio)
        # Publish user input to MQTT broker
        mqtt_client = connect()
        publish(mqtt_client, argumento_envio)
        mqtt_client.disconnect()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))