import { ASSET_STATUSES, ASSET_TYPES, STATUS_LABELS, TYPE_LABELS, type AssetStatus, type AssetType } from "../../api/patrimoine";

export interface AssetForm {
  reference: string;
  name: string;
  project: string;
  type: string;
  status: string;
  owner: string;
  description: string;
}

export const emptyAsset = (): AssetForm => ({
  reference: "",
  name: "",
  project: "",
  type: "cas_de_test",
  status: "brouillon",
  owner: "",
  description: "",
});

const inputClass = "w-full rounded-md border border-slate-300 px-3 py-2 text-sm";
const labelClass = "mb-1 block text-xs font-medium uppercase tracking-wide text-slate-500";

export const AssetFields = ({
  asset,
  onChange,
  referenceEditable = true,
}: {
  asset: AssetForm;
  onChange: (asset: AssetForm) => void;
  referenceEditable?: boolean;
}) => (
  <div className="grid gap-4 md:grid-cols-2">
    <div>
      <label className={labelClass} htmlFor="reference">Référence</label>
      <input
        id="reference"
        className={`${inputClass} font-mono`}
        placeholder="TC-001"
        required
        value={asset.reference}
        disabled={!referenceEditable}
        onChange={(event) => onChange({ ...asset, reference: event.target.value })}
      />
    </div>
    <div>
      <label className={labelClass} htmlFor="name">Nom</label>
      <input
        id="name"
        className={inputClass}
        placeholder="Nom de l'actif"
        required
        value={asset.name}
        onChange={(event) => onChange({ ...asset, name: event.target.value })}
      />
    </div>
    <div>
      <label className={labelClass} htmlFor="project">Projet</label>
      <input
        id="project"
        className={inputClass}
        placeholder="Projet"
        value={asset.project}
        onChange={(event) => onChange({ ...asset, project: event.target.value })}
      />
    </div>
    <div>
      <label className={labelClass} htmlFor="owner">Responsable</label>
      <input
        id="owner"
        className={inputClass}
        placeholder="Responsable"
        value={asset.owner}
        onChange={(event) => onChange({ ...asset, owner: event.target.value })}
      />
    </div>
    <div>
      <label className={labelClass} htmlFor="type">Type</label>
      <select
        id="type"
        className={inputClass}
        value={asset.type}
        onChange={(event) => onChange({ ...asset, type: event.target.value })}
      >
        {ASSET_TYPES.map((type: AssetType) => (
          <option key={type} value={type}>{TYPE_LABELS[type]}</option>
        ))}
      </select>
    </div>
    <div>
      <label className={labelClass} htmlFor="status">Statut</label>
      <select
        id="status"
        className={inputClass}
        value={asset.status}
        onChange={(event) => onChange({ ...asset, status: event.target.value })}
      >
        {ASSET_STATUSES.map((status: AssetStatus) => (
          <option key={status} value={status}>{STATUS_LABELS[status]}</option>
        ))}
      </select>
    </div>
    <div className="md:col-span-2">
      <label className={labelClass} htmlFor="description">Description</label>
      <textarea
        id="description"
        className={inputClass}
        rows={4}
        value={asset.description}
        onChange={(event) => onChange({ ...asset, description: event.target.value })}
      />
    </div>
  </div>
);
