"""Le patrimoine de test : l'inventaire des actifs de test (cas, exigences, campagnes).

Segment ``v1`` : les chemins servis ici sont ``/api/v1/...``.
"""

from fastapi import params

segment = "v1"

# L'app s'utilise dans un navigateur via la passerelle, sans appelant identifié : la règle d'accès
# est une déclaration explicite, et vide veut dire « servi sans appelant », pas « public par défaut ».
dependencies: tuple[params.Depends, ...] = ()
