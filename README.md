# Patrimoine de test — Microsquash

Application Mistral Studio de gestion du patrimoine de test (cas de test, exigences, campagnes) :

- **Inventaire** : recherche plein texte, filtres par projet, type et statut.
- **Cycle de vie** : création, modification, passage de statut (brouillon → relu → exécuté → archivé), suppression.
- **Tableau de bord** : volumétrie par statut, type et projet.
- **Import / export CSV** (séparateur `;`, compatible Excel fr).

## Structure

| Emplacement | Contenu |
| --- | --- |
| `apps/api` | API FastAPI : routes `/api/v1/assets`, `/api/v1/stats`, import/export. |
| `apps/web` | Interface TanStack Start : inventaire (`/assets`), création (`/assets/new`), fiche (`/assets/$assetId`). |
| `packages/py/db` | Modèle `test_assets`, accès base de données, migration Alembic `pat01_test_assets`. |

## Développer

```bash
mistral dev          # API + web + Postgres (Docker requis)
```

API sur `http://localhost:3000/api`, web sur `http://localhost:3001`.

## Déployer

```bash
mistral login
git add -A && git commit -m "patrimoine" && git push
mistral deploy --name microsquash-by-chonk --organization <votre-organisation>
```

## Notes techniques

- Le fichier `uv.lock` n'est pas inclus (généré hors ligne) : le `Dockerfile.api` résout les
  dépendances à la construction. Pour revenir à un build figé, exécuter `uv lock` puis rétablir
  `--frozen` dans `deploy/docker/Dockerfile.api`.
- L'interface n'utilise pas le client OpenAPI généré ; elle porte son propre client typé
  (`apps/web/src/api/patrimoine.ts`). Après tout changement d'API, lancer
  `bunx nx run fastapi-tanstack-start:gen-types` pour régénérer le client si vous souhaitez
  l'adopter.

## Colonnes du CSV d'import

`reference` (obligatoire, unique) ; `name` (obligatoire) ; `project` ; `type`
(`cas_de_test`, `exigence`, `campagne`) ; `status` (`brouillon`, `relu`, `execute`, `archive`) ;
`owner` ; `description`. Les références existantes sont mises à jour, les autres créées.
