from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List



import crud, models, schemas
from database import SessionLocal, engine

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


@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/add_kit/", response_model=schemas.Kit)
def create_kit(kit: schemas.KitCreate, db: Session = Depends(get_db)):
    return crud.create_kit(db=db, kit=kit)

@app.get("/kit/", response_model=list[schemas.Kit])
def read_kit(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_kit(db, skip=skip, limit=limit)




@app.post("/add_cirurgia/", response_model=schemas.Cirurgia)
def create_cirurgia(cirurgia: schemas.CirurgiaCreate, db: Session = Depends(get_db)):
    return crud.create_cirurgia(db=db, cirurgia=cirurgia)

@app.get("/cirurgia/", response_model=list[schemas.Cirurgia])
def read_cirurgia(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cirurgia(db, skip=skip, limit=limit)


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
