/** Le client du patrimoine de test : un fetch typé vers /api/v1, sans dépendance au client généré. */

import { env } from "../env";

const BASE = `${env.VITE_API_URL.replace(/\/+$/u, "")}/api/v1`;

export const ASSET_TYPES = ["cas_de_test", "exigence", "campagne"] as const;
export const ASSET_STATUSES = ["brouillon", "relu", "execute", "archive"] as const;

export type AssetType = (typeof ASSET_TYPES)[number];
export type AssetStatus = (typeof ASSET_STATUSES)[number];

export const TYPE_LABELS: Record<AssetType, string> = {
  cas_de_test: "Cas de test",
  exigence: "Exigence",
  campagne: "Campagne",
};

export const STATUS_LABELS: Record<AssetStatus, string> = {
  brouillon: "Brouillon",
  relu: "Relu",
  execute: "Exécuté",
  archive: "Archivé",
};

export interface Asset {
  id: string;
  reference: string;
  name: string;
  project: string;
  type: AssetType;
  status: AssetStatus;
  owner: string | null;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface AssetFilters {
  q?: string;
  project?: string;
  type?: string;
  status?: string;
}

export interface AssetInput {
  reference: string;
  name: string;
  project: string;
  type: string;
  status: string;
  owner?: string | null;
  description?: string | null;
}

export interface Stats {
  by_project: Record<string, number>;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE}${path}`, init);

  if (!response.ok) {
    let detail = `La requête a échoué (${response.status}).`;

    try {
      const body = (await response.json()) as { detail?: unknown };
      if (typeof body.detail === "string") {
        detail = body.detail;
      }
    } catch {
      // le corps n'est pas du JSON : garder le message par défaut
    }
    throw new Error(detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

const query = (filters: AssetFilters): string => {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) {
      params.set(key, value);
    }
  }
  const encoded = params.toString();
  return encoded ? `?${encoded}` : "";
};

export const patrimoineApi = {
  list: (filters: AssetFilters) =>
    request<{ total: number; items: Asset[] }>(`/assets${query(filters)}`),

  get: (id: string) => request<Asset>(`/assets/${id}`),

  create: (asset: AssetInput) =>
    request<Asset>("/assets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(asset),
    }),

  update: (id: string, changes: Partial<AssetInput>) =>
    request<Asset>(`/assets/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(changes),
    }),

  remove: (id: string) => request<void>(`/assets/${id}`, { method: "DELETE" }),

  stats: () => request<Stats>("/stats"),

  importFile: async (file: File) => {
    const body = new FormData();
    body.append("file", file);
    return request<{ created: number; updated: number; errors: string[] }>("/assets/import", {
      method: "POST",
      body,
    });
  },

  exportUrl: (filters: AssetFilters) => `${BASE}/assets/export${query(filters)}`,
};
