import tkinter as tk
from tkinter import ttk
from queue import Queue
from threading import Thread

class Interface:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Mesure Sondes")
        self.root.geometry("400x300")

        # Champs utilisateur
        ttk.Label(root, text="Poste :").pack(pady=5)
        self.poste_var = tk.StringVar(value="A-ABE")
        ttk.Entry(root, textvariable=self.poste_var).pack()

        ttk.Label(root, text="Sonde :").pack(pady=5)
        self.sonde_var = tk.StringVar(value="PT100")
        ttk.Entry(root, textvariable=self.sonde_var).pack()

        ttk.Label(root, text="Opérateur :").pack(pady=5)
        self.operateur_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.operateur_var).pack()

        # Boutons
        ttk.Button(
            root, text="Mesure résistance 4 fils",
            command=lambda: self._lancer_mesure("resistance_4fils")
        ).pack(pady=10)

        ttk.Button(
            root, text="Mesure isolement",
            command=lambda: self._lancer_mesure("isolement")
        ).pack()

        # Zone de résultat
        self.resultat_label = ttk.Label(root, text="En attente...", foreground="blue")
        self.resultat_label.pack(pady=20)

    def _lancer_mesure(self, type_mesure: str):
        """Lance la mesure dans un thread."""
        poste = self.poste_var.get()
        sonde = self.sonde_var.get()
        operateur = self.operateur_var.get()

        thread = Thread(
            target=self.controller.lancer_mesure,
            args=(type_mesure, poste, sonde, operateur),
            daemon=True
        )
        thread.start()
        self.resultat_label.config(text="Mesure en cours...", foreground="blue")