"""Routeur : projets de recette."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/projets", tags=["projets"])


@router.get("", response_model=list[schemas.ProjetOut])
def lister(db: Session = Depends(get_db)):
    return db.query(models.Projet).order_by(models.Projet.nom).all()


@router.post("", response_model=schemas.ProjetOut, status_code=201)
def creer(payload: schemas.ProjetCreate, db: Session = Depends(get_db)):
    if db.query(models.Projet).filter(models.Projet.nom == payload.nom).first():
        raise HTTPException(409, "Un projet porte déjà ce nom")
    projet = models.Projet(**payload.model_dump())
    db.add(projet)
    db.commit()
    db.refresh(projet)
    return projet


@router.delete("/{projet_id}", status_code=204)
def supprimer(projet_id: int, db: Session = Depends(get_db)):
    projet = db.get(models.Projet, projet_id)
    if not projet:
        raise HTTPException(404, "Projet introuvable")
    db.delete(projet)
    db.commit()
