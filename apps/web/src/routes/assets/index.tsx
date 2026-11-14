import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import {
  ASSET_STATUSES,
  ASSET_TYPES,
  patrimoineApi,
  STATUS_LABELS,
  TYPE_LABELS,
  type Asset,
  type AssetStatus,
  type AssetType,
} from "../../api/patrimoine";

export const Route = createFileRoute("/assets/")({
  staticData: { landing: true },
  component: Inventory,
});

const STATUSES = ASSET_STATUSES as readonly AssetStatus[];
const TYPES = ASSET_TYPES as readonly AssetType[];

const statusBadge = (status: AssetStatus) =>
  ({
    brouillon: "bg-slate-100 text-slate-700",
    relu: "bg-blue-100 text-blue-700",
    execute: "bg-green-100 text-green-700",
    archive: "bg-amber-100 text-amber-700",
  })[status];

const Inventory = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [q, setQ] = useState("");
  const [project, setProject] = useState("");
  const [type, setType] = useState("");
  const [status, setStatus] = useState("");
  const [importMessage, setImportMessage] = useState<string | null>(null);

  const filters = { q, project, type, status };

  const assets = useQuery({
    queryKey: ["assets", filters],
    queryFn: () => patrimoineApi.list(filters),
  });
  const stats = useQuery({ queryKey: ["stats"], queryFn: () => patrimoineApi.stats() });

  const importMutation = useMutation({
    mutationFn: (file: File) => patrimoineApi.importFile(file),
    onSuccess: (report) => {
      setImportMessage(`Import : ${report.created} créé(s), ${report.updated} mis à jour.`);
      void queryClient.invalidateQueries();
    },
    onError: (error: Error) => setImportMessage(`Import échoué : ${error.message}`),
  });

  return (
    <main className="mx-auto max-w-6xl p-6">
      <header className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Patrimoine de test</h1>
          <p className="text-sm text-slate-600">Inventaire des cas de test, exigences et campagnes</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
            to="/assets/new"
          >
            + Nouvel actif
          </Link>
          <a
            className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-100"
            href={patrimoineApi.exportUrl(filters)}
          >
            Exporter en CSV
          </a>
          <label className="cursor-pointer rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-100">
            Importer un CSV
            <input
              className="hidden"
              type="file"
              accept=".csv,text/csv"
              onChange={(event) => {
                const file = event.target.files?.[0];
                if (file) {
                  importMutation.mutate(file);
                }
                event.target.value = "";
              }}
            />
          </label>
        </div>
      </header>

      {stats.data ? (
        <section className="mb-6 grid grid-cols-2 gap-3 md:grid-cols-4">
          <Card label="Actifs" value={Object.values(stats.data.by_status).reduce((a, b) => a + b, 0)} />
          {STATUSES.map((statusKey) => (
            <Card key={statusKey} label={STATUS_LABELS[statusKey]} value={stats.data.by_status[statusKey] ?? 0} />
          ))}
        </section>
      ) : null}

      <section className="mb-4 flex flex-wrap gap-2">
        <input
          className="w-56 rounded-md border border-slate-300 px-3 py-2 text-sm"
          placeholder="Rechercher…"
          value={q}
          onChange={(event) => setQ(event.target.value)}
        />
        <input
          className="w-44 rounded-md border border-slate-300 px-3 py-2 text-sm"
          placeholder="Projet"
          value={project}
          onChange={(event) => setProject(event.target.value)}
        />
        <select
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
          value={type}
          onChange={(event) => setType(event.target.value)}
        >
          <option value="">Tous les types</option>
          {TYPES.map((typeValue) => (
            <option key={typeValue} value={typeValue}>
              {TYPE_LABELS[typeValue]}
            </option>
          ))}
        </select>
        <select
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
          value={status}
          onChange={(event) => setStatus(event.target.value)}
        >
          <option value="">Tous les statuts</option>
          {STATUSES.map((statusValue) => (
            <option key={statusValue} value={statusValue}>
              {STATUS_LABELS[statusValue]}
            </option>
          ))}
        </select>
      </section>

      {importMessage ? <p className="mb-4 text-sm text-slate-700">{importMessage}</p> : null}

      {assets.isPending ? <p className="text-sm text-slate-500">Chargement…</p> : null}
      {assets.isError ? (
        <p className="text-sm text-red-600">Erreur : {(assets.error as Error).message}</p>
      ) : null}

      {assets.data ? (
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-3">Référence</th>
                <th className="px-4 py-3">Nom</th>
                <th className="px-4 py-3">Projet</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Statut</th>
                <th className="px-4 py-3">Responsable</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {assets.data.items.map((asset: Asset) => (
                <tr
                  key={asset.id}
                  className="cursor-pointer hover:bg-slate-50"
                  onClick={() => void navigate({ to: "/assets/$assetId", params: { assetId: asset.id } })}
                >
                  <td className="px-4 py-3 font-mono text-xs">{asset.reference}</td>
                  <td className="px-4 py-3">{asset.name}</td>
                  <td className="px-4 py-3">{asset.project}</td>
                  <td className="px-4 py-3">{TYPE_LABELS[asset.type as AssetType] ?? asset.type}</td>
                  <td className="px-4 py-3">
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusBadge(asset.status as AssetStatus)}`}>
                      {STATUS_LABELS[asset.status as AssetStatus] ?? asset.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">{asset.owner ?? "—"}</td>
                </tr>
              ))}
              {assets.data.items.length === 0 ? (
                <tr>
                  <td className="px-4 py-6 text-center text-slate-500" colSpan={6}>
                    Aucun actif ne correspond aux filtres.
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      ) : null}
    </main>
  );
};

const Card = ({ label, value }: { label: string; value: number }) => (
  <div className="rounded-lg border border-slate-200 p-4">
    <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
    <p className="text-2xl font-semibold">{value}</p>
  </div>
);
