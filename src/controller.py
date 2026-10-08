from model.mesures import MesureResistance, MesureIsolement
from model.appareils import AppareilKeysight
from model.excel_saver import ExcelSaver
from queue import Queue

class Controller:
    def __init__(self):
        self.appareil_resistance = AppareilKeysight("USB0::0x0957::0x1807::MY57206438::INSTR")
        self.appareil_isolement = AppareilKeysight("USB0::0x0957::0x1730::MY53200023::INSTR")
        self.excel_saver = ExcelSaver()

    def lancer_mesure(self, type_mesure: str, poste: str, sonde: str, operateur: str):
        """Coordinator entre model et view."""
        try:
            if not self.appareil_resistance.est_connecte() or not self.appareil_isolement.est_connecte():
                raise RuntimeError("Un appareil n'est pas connecté !")

            if type_mesure == "resistance_4fils":
                mesure = MesureResistance(type_mesure, poste, sonde, operateur).lancer(self.appareil_resistance)
            elif type_mesure == "isolement":
                mesure = MesureIsolement(type_mesure, poste, sonde, operateur).lancer(self.appareil_isolement)

            self.excel_saver.sauvegarder(mesure)
            return mesure
        except Exception as e:
            return str(e)