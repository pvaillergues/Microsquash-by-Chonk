"""Routeur : inventaire des cas de test (CRUD + recherche)."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/cas-de-test", tags=["cas-de-test"])


@router.get("", response_model=list[schemas.CasDeTestOut])
def lister(
    db: Session = Depends(get_db),
    projet_id: Optional[int] = None,
    statut: Optional[str] = None,
    criticite: Optional[str] = None,
    q: Optional[str] = Query(None, description="Recherche plein texte sur référence et nom"),
):
    req = db.query(models.CasDeTest)
    if projet_id:
        req = req.filter(models.CasDeTest.projet_id == projet_id)
    if statut:
        req = req.filter(models.CasDeTest.statut == statut)
    if criticite:
        req = req.filter(models.CasDeTest.criticite == criticite)
    if q:
        like = f"%{q}%"
        req = req.filter(or_(models.CasDeTest.reference.ilike(like), models.CasDeTest.nom.ilike(like)))
    return req.order_by(models.CasDeTest.reference).all()


@router.get("/{cas_id}", response_model=schemas.CasDeTestOut)
def detail(cas_id: int, db: Session = Depends(get_db)):
    cas = db.get(models.CasDeTest, cas_id)
    if not cas:
        raise HTTPException(404, "Cas de test introuvable")
    return cas


@router.post("", response_model=schemas.CasDeTestOut, status_code=201)
def creer(payload: schemas.CasDeTestCreate, db: Session = Depends(get_db)):
    if not db.get(models.Projet, payload.projet_id):
        raise HTTPException(400, "Projet inexistant")
    if db.query(models.CasDeTest).filter(models.CasDeTest.reference == payload.reference).first():
        raise HTTPException(409, "Référence déjà utilisée")
    cas = models.CasDeTest(**payload.model_dump())
    db.add(cas)
    db.commit()
    db.refresh(cas)
    return cas


@router.put("/{cas_id}", response_model=schemas.CasDeTestOut)
def modifier(cas_id: int, payload: schemas.CasDeTestBase, db: Session = Depends(get_db)):
    cas = db.get(models.CasDeTest, cas_id)
    if not cas:
        raise HTTPException(404, "Cas de test introuvable")
    for k, v in payload.model_dump().items():
        setattr(cas, k, v)
    db.commit()
    db.refresh(cas)
    return cas


@router.delete("/{cas_id}", status_code=204)
def supprimer(cas_id: int, db: Session = Depends(get_db)):
    cas = db.get(models.CasDeTest, cas_id)
    if not cas:
        raise HTTPException(404, "Cas de test introuvable")
    db.delete(cas)
    db.commit()
