"""Worker workflows : traitement asynchrone du patrimoine de test.

Exemple de workflow : recalcul nocturne de l'avancement des campagnes,
synchronisation d'imports en masse. À adapter au SDK workflows Mistral
généré par la capacité `workflows`.

Structure générée par `mistral init --preset app` — le squelette ci-dessous
illustre le point d'entrée typique.

from mistral_workflows import workflow

@workflow
def recalculer_avancement(context):
    """Parcourt les campagnes et met à jour leurs taux d'avancement."""
    ...
