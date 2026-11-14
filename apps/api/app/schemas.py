"""Schémas Pydantic de l'API."""
import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjetBase(BaseModel):
    nom: str
    description: str = ""


class ProjetCreate(ProjetBase):
    pass


class ProjetOut(ProjetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime


class CasDeTestBase(BaseModel):
    reference: str
    nom: str
    description: str = ""
    statut: str = "EN_COURS"
    criticite: str = "MOYENNE"


class CasDeTestCreate(CasDeTestBase):
    projet_id: int


class CasDeTestOut(CasDeTestBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    projet_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CampagneBase(BaseModel):
    nom: str
    iteration: str = ""
    date_debut: Optional[datetime.date] = None
    date_fin: Optional[datetime.date] = None


class CampagneCreate(CampagneBase):
    projet_id: int


class CampagneOut(CampagneBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    projet_id: int


class ExecutionCreate(BaseModel):
    cas_de_test_id: int
    statut: str = "A_EXECUTER"


class ExecutionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    campagne_id: int
    cas_de_test_id: int
    statut: str
    executed_at: Optional[datetime.datetime] = None
