#!/usr/bin/env python3
"""Convertit les lectures du Sheet « Registre de veille réglementaire QSE/RSE – SATA »
en data/veille.json, le fichier lu par index.html.

Usage :
  python3 scripts/sheet_to_json.py --veille veille_raw.json --journal journal_raw.json \
      --out data/veille.json

veille_raw.json / journal_raw.json : la valeur renvoyée par readCells (objet avec
une clé "rows" indexée par numéro de ligne, ligne 1 = en-têtes) pour les onglets
« Veille » (A1:Q…) et « Journal des veilles » (A1:F…).

Seules les colonnes publiques sont exportées : pas de pilote, et rien de l'onglet
« Exigences applicables » (état de conformité interne).
"""
import argparse
import json
from datetime import datetime
from zoneinfo import ZoneInfo

VEILLE_COLS = [
    "id", "detecte", "intitule", "domaine", "applicabilite", "criticite",
    "vigueur", "action", "echeance", "statut", "type", "reference", "resume",
    "sites", "_pilote", "lien", "publie",
]
JOURNAL_COLS = ["date", "periode", "detectes", "applicables", "eleves", "faits"]


def cell(v):
    """Ramène une cellule lue par readCells à une valeur simple."""
    if v is None:
        return None
    if isinstance(v, dict):
        if "date" in v:
            return v["date"]
        if "dateTime" in v:
            return v["dateTime"][:10]
        if "value" in v:
            return cell(v["value"])
        if "number" in v:
            return v["number"]
        if "markdown" in v:
            return v["markdown"]
        return None
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def rows_of(raw, cols):
    rows = raw.get("rows", raw)
    out = []
    for key in sorted(rows, key=lambda k: int(k)):
        if int(key) == 1:
            continue  # en-têtes
        values = [cell(v) for v in rows[key]]
        values += [None] * (len(cols) - len(values))
        rec = {c: values[i] for i, c in enumerate(cols) if not c.startswith("_")}
        if any(v not in (None, "") for v in rec.values()):
            out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--veille", required=True)
    ap.add_argument("--journal")
    ap.add_argument("--out", default="data/veille.json")
    ap.add_argument("--updated-at", help="ISO 8601 ; par défaut maintenant (Europe/Paris)")
    a = ap.parse_args()

    with open(a.veille, encoding="utf-8") as f:
        textes = [t for t in rows_of(json.load(f), VEILLE_COLS) if t.get("id")]
    journal = []
    if a.journal:
        with open(a.journal, encoding="utf-8") as f:
            journal = [j for j in rows_of(json.load(f), JOURNAL_COLS) if j.get("date")]

    updated = a.updated_at or datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="minutes")
    data = {
        "meta": {
            "updated_at": updated,
            "source": "Registre de veille réglementaire QSE/RSE – SATA",
            "count": len(textes),
        },
        "textes": textes,
        "journal": journal,
    }
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{len(textes)} textes, {len(journal)} entrées de journal -> {a.out} (maj {updated})")


if __name__ == "__main__":
    main()
