import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useState } from 'react'

type CasDeTest = {
  id: number
  reference: string
  nom: string
  statut: string
  criticite: string
  projet_id: number
}

const STATUTS = ['BROUILLON', 'EN_COURS', 'TERMINE', 'ARCHIVE']
const CRITICITES = ['MINEURE', 'MOYENNE', 'MAJEURE', 'CRITIQUE']

export const Route = createFileRoute('/')({
  component: Inventaire,
})

function Inventaire() {
  const [cas, setCas] = useState<CasDeTest[]>([])
  const [q, setQ] = useState('')
  const [statut, setStatut] = useState('')
  const [criticite, setCriticite] = useState('')
  const [chargement, setChargement] = useState(true)

  useEffect(() => {
    const params = new URLSearchParams()
    if (q) params.set('q', q)
    if (statut) params.set('statut', statut)
    if (criticite) params.set('criticite', criticite)
    fetch(`/api/cas-de-test?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setCas(data)
        setChargement(false)
      })
      .catch(() => setChargement(false))
  }, [q, statut, criticite])

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Patrimoine de test</h1>

      <div className="flex gap-3 mb-4">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Rechercher (référence, nom)…"
          className="border rounded px-3 py-2 flex-1"
        />
        <select value={statut} onChange={(e) => setStatut(e.target.value)} className="border rounded px-3 py-2">
          <option value="">Tous statuts</option>
          {STATUTS.map((s) => <option key={s}>{s}</option>)}
        </select>
        <select value={criticite} onChange={(e) => setCriticite(e.target.value)} className="border rounded px-3 py-2">
          <option value="">Toutes criticités</option>
          {CRITICITES.map((c) => <option key={c}>{c}</option>)}
        </select>
      </div>

      {chargement ? (
        <p>Chargement…</p>
      ) : (
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2">Référence</th>
              <th>Nom</th>
              <th>Statut</th>
              <th>Criticité</th>
            </tr>
          </thead>
          <tbody>
            {cas.map((c) => (
              <tr key={c.id} className="border-b hover:bg-gray-50">
                <td className="py-2 font-mono">{c.reference}</td>
                <td>{c.nom}</td>
                <td>{c.statut}</td>
                <td>{c.criticite}</td>
              </tr>
            ))}
            {cas.length === 0 && (
              <tr><td colSpan={4} className="py-4 text-center text-gray-500">Aucun cas de test</td></tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  )
}
