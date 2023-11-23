from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import ssl
import time
import paho.mqtt.client as mqtt_client
from crud import create_kit, get_kit, create_cirurgia, get_cirurgia
from database import SessionLocal, engine
import schemas

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware for handling Cross-Origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# MQTT configuration
mqtt_broker_address = "your_mqtt_broker_address"
mqtt_port = 1883
mqtt_topic = "your_mqtt_topic"

def connect() -> mqtt_client.Client:
    mqtt_client_id = "fastapi-mqtt-client"
    mqtt_client = mqtt_client.Client(client_id=mqtt_client_id)
    mqtt_client.connect(mqtt_broker_address, mqtt_port)
    return mqtt_client

def publish(mqtt_client: mqtt_client.Client, message: str):
    mqtt_client.publish(mqtt_topic, message)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/add_kit/", response_model=schemas.Kit)
def create_kit(kit: schemas.KitCreate, db: Session = Depends(get_db)):
    return create_kit(db=db, kit=kit)

@app.get("/kit/", response_model=List[schemas.Kit])
def read_kit(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_kit(db, skip=skip, limit=limit)

@app.post("/add_cirurgia/", response_model=schemas.Cirurgia)
def create_cirurgia(cirurgia: schemas.CirurgiaCreate, db: Session = Depends(get_db)):
    return create_cirurgia(db=db, cirurgia=cirurgia)

@app.get("/cirurgia/", response_model=List[schemas.Cirurgia])
def read_cirurgia(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_cirurgia(db, skip=skip, limit=limit)

@app.post("/e/")
async def process_form(request: Request):
    try:
        argumento_envio = await request.json()
        print(argumento_envio["kit"])
        # Publish user input to MQTT broker
        mqtt_client_instance = connect()
        publish(mqtt_client_instance, argumento_envio["kit"])
        mqtt_client_instance.disconnect()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))