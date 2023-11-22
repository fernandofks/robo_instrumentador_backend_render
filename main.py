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



# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)



templates = Jinja2Templates(directory="templates")

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



# def publish(client, message):
#     msg_count = 1
#     while True:
#         time.sleep(1)
#         result = client.publish(topic, message, 0)
#         status = result[0]
#         if status == 0:
#             print(f"Sent `{message}` to topic `{topic}`")
#         else:
#             print(f"Failed to send message to topic {topic}")
#         msg_count += 1
#         if msg_count > 50:
#             break

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/add_kit/", response_model=schemas.Kit)
def create_kit(kit: schemas.KitCreate, db: Session = Depends(get_db)):
    return crud.create_kit(db=db, kit=kit)

@app.get("/kit/", response_model=List[schemas.Kit])
def read_kit(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_kit(db, skip=skip, limit=limit)



@app.post("/add_cirurgia/", response_model=schemas.Cirurgia)
def create_cirurgia(cirurgia: schemas.CirurgiaCreate, db: Session = Depends(get_db)):
    return crud.create_cirurgia(db=db, cirurgia=cirurgia)

@app.get("/cirurgia/", response_model=List[schemas.Cirurgia])
def read_cirurgia(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cirurgia(db, skip=skip, limit=limit)


# @app.post("/envio_mqtt")
# def process_form():
#     user_input = "tesoura"
#     # Publish user input to MQTT broker
#     mqtt_client = connect()
#     publish(mqtt_client, user_input)
#     print("supostamente")
#     mqtt_client.disconnect()
#     return 0



# @app.post("/e/")
# def process_form(request: Request):
#     argumento_envio = await request.json()
#     print(argumento_envio["kit"])
#     # Publish user input to MQTT broker
#     mqtt_client = connect()
#     publish(mqtt_client, argumento_envio["kit"])
#     mqtt_client.disconnect()


@app.post("/e/")
async def process_form(request: Request):
    try:
        argumento_envio = await request.json()
        print(argumento_envio["kit"])
        # Publish user input to MQTT broker
        mqtt_client = connect()
        publish(mqtt_client, argumento_envio["kit"])
        mqtt_client.disconnect()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))



# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items




