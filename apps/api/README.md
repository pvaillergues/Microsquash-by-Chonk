# API — Gestion du patrimoine de test

FastAPI + SQLAlchemy sur la base Postgres (capacité `postgres`).

## Installation locale

    cd apps/api
    uv sync            # ou : pip install -r requirements.txt
    uvicorn app.main:app --reload

## Endpoints principaux

- GET  /api/health — état de l'API
- GET  /api/projets — projets de recette
- GET  /api/cas-de-test?q=&statut=&criticite=&projet_id= — inventaire filtrable
- POST /api/cas-de-test — création (référence unique, ex. CPT-001)
- GET  /api/campagnes?projet_id= — campagnes
- POST /api/campagnes/{id}/executions — ajouter une exécution
- GET  /api/campagnes/{id}/avancement — avancement par statut

Documentation interactive : http://localhost:8000/docs
