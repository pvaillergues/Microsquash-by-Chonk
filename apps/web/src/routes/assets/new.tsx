import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { ASSET_STATUSES, ASSET_TYPES, patrimoineApi, STATUS_LABELS, TYPE_LABELS } from "../../api/patrimoine";
import { AssetFields, emptyAsset } from "./-shared";

export const Route = createFileRoute("/assets/new")({
  component: NewAsset,
});

function NewAsset() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [asset, setAsset] = useState(emptyAsset());
  const [error, setError] = useState<string | null>(null);

  const create = useMutation({
    mutationFn: () =>
      patrimoineApi.create({
        ...asset,
        owner: asset.owner || null,
        description: asset.description || null,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries();
      void navigate({ to: "/assets" });
    },
    onError: (mutationError: Error) => setError(mutationError.message),
  });

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="mb-6 text-2xl font-semibold">Nouvel actif de test</h1>
      {error ? <p className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p> : null}
      <AssetFields asset={asset} onChange={setAsset} />
      <div className="mt-6 flex gap-2">
        <button
          className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
          disabled={create.isPending}
          onClick={() => create.mutate()}
          type="button"
        >
          Créer
        </button>
        <button
          className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-100"
          onClick={() => void navigate({ to: "/assets" })}
          type="button"
        >
          Annuler
        </button>
      </div>
      <p className="mt-6 text-xs text-slate-400">
        Types : {ASSET_TYPES.map((type) => TYPE_LABELS[type]).join(", ")} · Statuts :{" "}
        {ASSET_STATUSES.map((status) => STATUS_LABELS[status]).join(", ")}
      </p>
    </main>
  );
}
