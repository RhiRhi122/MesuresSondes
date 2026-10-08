import sys
from pathlib import Path

# Ajoute le répertoire parent au chemin Python
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.model.isolation import IsolationTester, ResultatIsolement

def main():
    """Teste le module de test d'isolement."""
    print("🔧 Initialisation du testeur d'isolement...")
    print("-" * 70)

    # Initialisation du testeur
    testeur = IsolationTester(simulateur=True)

    # Liste de sondes à tester (peut être chargée depuis postes.json)
    sondes_a_tester = [
        "TX-101", "TX-102", "TP-201", "FG-001_WFb",
        "HTR-101", "PZ-001_C", "LT-001", "TLS-001_W1"
    ]

    print(f"📊 Test d'isolement pour {len(sondes_a_tester)} sondes:")
    print("-" * 70)

    # Exécution des tests
    for sonde_id in sondes_a_tester:
        try:
            resultat = testeur.mesurer_isolement(sonde_id, operateur="RhiRhi")
            print(f"🔹 Sonde: {resultat.id_sondes}")
            print(f"   Résistance d'isolement: {resultat.resistance/1000000:.2f} MΩ")
            print(f"   Statut: {'✅ OK' if resultat.statut == 'OK' else '❌ ERREUR'}")
            print(f"   Limite minimale: {resultat.limite_min/1000000:.0f} MΩ")
            print(f"   Opérateur: {resultat.operateur}")
            print(f"   Date/Heure: {resultat.date_heure}")
            print("-" * 70)
        except Exception as e:
            print(f"❌ Erreur lors du test d'isolement pour {sonde_id}: {e}")
            print("-" * 70)

if __name__ == "__main__":
    main()