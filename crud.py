from sqlalchemy.orm import Session

import models, schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

def get_kit(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kit).offset(skip).limit(limit).all()

def get_cirurgia(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cirurgia).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def create_kit(db: Session, kit: schemas.KitCreate):
    db_kit = models.Kit(nome_instrumento=kit.nome_instrumento)
    db.add(db_kit)
    db.commit()
    db.refresh(db_kit)
    return db_kit


def create_cirurgia(db: Session, cirurgia: schemas.CirurgiaCreate):
    db_cirurgia = models.Cirurgia(CRM_Medico=cirurgia.CRM_Medico, CPF_Paciente=cirurgia.CPF_Paciente, Sala_Hospital=cirurgia.Sala_Hospital, Tipo_Cirurgia=cirurgia.Tipo_Cirurgia, Kit_id=cirurgia.Kit_id)
    db.add(db_cirurgia)
    db.commit()
    db.refresh(db_cirurgia)
    return db_cirurgia



# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
