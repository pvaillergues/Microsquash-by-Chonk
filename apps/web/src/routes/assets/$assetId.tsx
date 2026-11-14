import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { patrimoineApi, STATUS_LABELS, TYPE_LABELS, type AssetStatus, type AssetType } from "../../api/patrimoine";
import { AssetFields, type AssetForm } from "./-shared";

export const Route = createFileRoute("/assets/$assetId")({
  component: AssetDetail,
});

const toForm = (asset: {
  reference: string;
  name: string;
  project: string;
  type: string;
  status: string;
  owner: string | null;
  description: string | null;
}): AssetForm => ({
  reference: asset.reference,
  name: asset.name,
  project: asset.project,
  type: asset.type,
  status: asset.status,
  owner: asset.owner ?? "",
  description: asset.description ?? "",
});

function AssetDetail() {
  const { assetId } = Route.useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  const asset = useQuery({
    queryKey: ["asset", assetId],
    queryFn: () => patrimoineApi.get(assetId),
  });
  const [form, setForm] = useState<AssetForm | null>(null);

  const save = useMutation({
    mutationFn: (current: AssetForm) =>
      patrimoineApi.update(assetId, {
        name: current.name,
        project: current.project,
        type: current.type,
        status: current.status,
        owner: current.owner || null,
        description: current.description || null,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries();
      void navigate({ to: "/assets" });
    },
    onError: (mutationError: Error) => setError(mutationError.message),
  });

  const remove = useMutation({
    mutationFn: () => patrimoineApi.remove(assetId),
    onSuccess: () => {
      void queryClient.invalidateQueries();
      void navigate({ to: "/assets" });
    },
    onError: (mutationError: Error) => setError(mutationError.message),
  });

  if (asset.isPending) {
    return <main className="mx-auto max-w-2xl p-6"><p className="text-sm text-slate-500">Chargement…</p></main>;
  }
  if (asset.isError || !asset.data) {
    return (
      <main className="mx-auto max-w-2xl p-6">
        <p className="text-sm text-red-600">Actif introuvable.</p>
      </main>
    );
  }

  const current = form ?? toForm(asset.data);
  const changed = form !== null;

  return (
    <main className="mx-auto max-w-2xl p-6">
      <p className="text-sm text-slate-500">
        {TYPE_LABELS[asset.data.type as AssetType] ?? asset.data.type} ·{" "}
        {STATUS_LABELS[asset.data.status as AssetStatus] ?? asset.data.status} ·{" "}
        créé le {new Date(asset.data.created_at).toLocaleDateString("fr-FR")}
      </p>
      <h1 className="mb-1 text-2xl font-semibold">{asset.data.name}</h1>
      <p className="mb-6 font-mono text-sm text-slate-500">{asset.data.reference}</p>

      {error ? <p className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p> : null}

      <AssetFields asset={current} onChange={setForm} referenceEditable={false} />

      <div className="mt-6 flex gap-2">
        <button
          className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
          disabled={!changed || save.isPending}
          onClick={() => save.mutate(current)}
          type="button"
        >
          Enregistrer
        </button>
        <button
          className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-100"
          onClick={() => void navigate({ to: "/assets" })}
          type="button"
        >
          Retour
        </button>
        <button
          className="ml-auto rounded-md border border-red-200 px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-50"
          onClick={() => remove.mutate()}
          type="button"
        >
          Supprimer
        </button>
      </div>
    </main>
  );
}
