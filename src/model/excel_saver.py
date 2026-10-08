import pandas as pd
from pathlib import Path

class ExcelSaver:
    def __init__(self, fichier: str = "data/mesures.xlsx"):
        self.fichier = Path(fichier)
        if not self.fichier.exists():
            pd.DataFrame(columns=[
                "Date", "Heure", "Opérateur", "Poste", "Sonde",
                "Type", "Valeur (Ω)", "Statut"
            ]).to_excel(self.fichier, index=False)

    def sauvegarder(self, mesure: Mesure):
        """Ajoute une mesure au fichier Excel."""
        df = pd.read_excel(self.fichier)
        nouvelle_ligne = {
            "Date": mesure.date_heure.split()[0],
            "Heure": mesure.date_heure.split()[1],
            "Opérateur": mesure.operateur,
            "Poste": mesure.poste,
            "Sonde": mesure.sonde,
            "Type": mesure.type,
            "Valeur (Ω)": mesure.valeur,
            "Statut": mesure.statut
        }
        df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
        df.to_excel(self.fichier, index=False)