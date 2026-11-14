# Patrimoine de test — App Studio (Microsquash by Chonk)

Application de gestion du patrimoine de test (cas de test, campagnes, exécutions),
construite avec Mistral Studio Apps.

- `apps/web` — frontend TanStack Start (vue inventaire avec recherche et filtres)
- `apps/api` — API FastAPI (CRUD cas de test, projets, campagnes, avancement)
- `apps/worker` — worker de workflows (imports, recalculs)
- Base Postgres (capacité `postgres`)

## Mise en place

    mistral login
    mistral init patrimoine-test --preset app   # ou dans ce dépôt cloné
    # renseigner MISTRAL_API_KEY dans .env
    mistral dev

## Déployer

    git push
    mistral deploy

Les secrets (ex. MISTRAL_API_KEY) se règlent dans l'onglet Secrets de l'app dans Studio.

## Prochaines étapes

- [ ] Import CSV/Excel depuis SquashTM
- [ ] Vue détail d'un cas de test (pas à pas, exigences liées)
- [ ] Tableau de bord qualité (taux de réussite par campagne)
- [ ] Authentification et rôles
