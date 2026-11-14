"""Modèles du patrimoine de test (aligné sur les concepts SquashTM)."""
import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Projet(Base):
    __tablename__ = "projets"

    id = Column(Integer, primary_key=True)
    nom = Column(String(200), nullable=False, unique=True)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    cas_de_test = relationship("CasDeTest", back_populates="projet", cascade="all, delete-orphan")
    campagnes = relationship("Campagne", back_populates="projet", cascade="all, delete-orphan")


class CasDeTest(Base):
    __tablename__ = "cas_de_test"

    id = Column(Integer, primary_key=True)
    reference = Column(String(50), nullable=False, unique=True)  # ex: CPT-001
    nom = Column(String(300), nullable=False)
    description = Column(Text, default="")
    statut = Column(String(30), default="EN_COURS")  # BROUILLON | EN_COURS | TERMINE | ARCHIVE
    criticite = Column(String(30), default="MOYENNE")  # MINEURE | MOYENNE | MAJEURE | CRITIQUE
    projet_id = Column(Integer, ForeignKey("projets.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    projet = relationship("Projet", back_populates="cas_de_test")


class Campagne(Base):
    __tablename__ = "campagnes"

    id = Column(Integer, primary_key=True)
    nom = Column(String(200), nullable=False)
    iteration = Column(String(100), default="")
    date_debut = Column(Date, nullable=True)
    date_fin = Column(Date, nullable=True)
    projet_id = Column(Integer, ForeignKey("projets.id"), nullable=False)

    projet = relationship("Projet", back_populates="campagnes")
    executions = relationship("Execution", back_populates="campagne", cascade="all, delete-orphan")


class Execution(Base):
    """Résultat d'exécution d'un cas de test dans une campagne."""
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True)
    campagne_id = Column(Integer, ForeignKey("campagnes.id"), nullable=False)
    cas_de_test_id = Column(Integer, ForeignKey("cas_de_test.id"), nullable=False)
    statut = Column(String(30), default="A_EXECUTER")  # A_EXECUTER | REUSSI | ECHEC | BLOQUE | ANNULE
    executed_at = Column(DateTime, nullable=True)

    campagne = relationship("Campagne", back_populates="executions")
    cas_de_test = relationship("CasDeTest")
