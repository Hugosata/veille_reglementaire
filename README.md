# Veille réglementaire QSE/RSE – SATA

Page publique de consultation de la veille réglementaire QSE/RSE des domaines skiables SATA
(Les 2 Alpes, Alpe d'Huez, La Grave, Alpe du Grand Serre).

- `index.html` : la page (aucune dépendance, lit `data/veille.json`).
- `data/veille.json` : les données, régénérées chaque lundi par la routine de veille.
- `scripts/sheet_to_json.py` : convertit les onglets « Veille » et « Journal des veilles » du registre en `data/veille.json`.

Source de travail : le registre de veille (Sheet Claude), où le service QSE/RSE met à jour
statuts et analyses. Cette page n'en publie que la partie veille : ni pilotes, ni état de conformité.

Information indicative : toujours vérifier le texte officiel avant décision.
