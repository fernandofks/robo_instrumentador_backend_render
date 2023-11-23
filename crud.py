from sqlalchemy.orm import Session

import models, schemas

def get_kit(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kit).offset(skip).limit(limit).all()

def get_cirurgia(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cirurgia).offset(skip).limit(limit).all()

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