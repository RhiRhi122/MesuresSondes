import pyvisa

class AppareilKeysight:
    def __init__(self, adresse: str):
        self.rm = pyvisa.ResourceManager()
        try:
            self.instrument = self.rm.open_resource(adresse)
            self.instrument.timeout = 5000  # 5s de timeout
        except Exception as e:
            raise RuntimeError(f"Appareil non connecté : {adresse}") from e

    def lire_resistance(self, type_mesure: str) -> float:
        """Lit la résistance via SCPI (exemple pour 34972A)."""
        if type_mesure == "resistance_4fils":
            self.instrument.write(":SENS:FUNC 'RES', (@101)")
        elif type_mesure == "isolement":
            self.instrument.write(":SENS:FUNC 'VOLT:DC', (@102)")
        return float(self.instrument.query(":READ?"))

    def est_connecte(self) -> bool:
        """Vérifie si l'appareil répond."""
        try:
            self.instrument.query("*IDN?")
            return True
        except:
            return False

    def test_connexion(self):
        """Teste si l'appareil répond."""
        try:
            self.instrument.query("*IDN?")  # Demande l'identifiant
            return True
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return False