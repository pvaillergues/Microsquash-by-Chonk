"""Routeur : campagnes et exécutions."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/campagnes", tags=["campagnes"])


@router.get("", response_model=list[schemas.CampagneOut])
def lister(projet_id: int = None, db: Session = Depends(get_db)):
    req = db.query(models.Campagne)
    if projet_id:
        req = req.filter(models.Campagne.projet_id == projet_id)
    return req.order_by(models.Campagne.nom).all()


@router.post("", response_model=schemas.CampagneOut, status_code=201)
def creer(payload: schemas.CampagneCreate, db: Session = Depends(get_db)):
    if not db.get(models.Projet, payload.projet_id):
        raise HTTPException(400, "Projet inexistant")
    campagne = models.Campagne(**payload.model_dump())
    db.add(campagne)
    db.commit()
    db.refresh(campagne)
    return campagne


@router.post("/{campagne_id}/executions", response_model=schemas.ExecutionOut, status_code=201)
def ajouter_execution(campagne_id: int, payload: schemas.ExecutionCreate, db: Session = Depends(get_db)):
    campagne = db.get(models.Campagne, campagne_id)
    if not campagne:
        raise HTTPException(404, "Campagne introuvable")
    if not db.get(models.CasDeTest, payload.cas_de_test_id):
        raise HTTPException(400, "Cas de test inexistant")
    execution = models.Execution(campagne_id=campagne_id, **payload.model_dump())
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return execution


@router.get("/{campagne_id}/avancement")
def avancement(campagne_id: int, db: Session = Depends(get_db)):
    executions = db.query(models.Execution).filter(models.Execution.campagne_id == campagne_id).all()
    total = len(executions)
    par_statut = {}
    for e in executions:
        par_statut[e.statut] = par_statut.get(e.statut, 0) + 1
    return {"total": total, "par_statut": par_statut}
