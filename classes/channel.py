#channel.py

import tkinter as tk
import mysql.connector

class GestionnaireCanaux(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des canaux Discord")
        self.geometry("800x600")

        # Connexion à la base de données MySQL
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydiscord"
        )
        self.curseur = self.connexion.cursor()
        
        # Interface utilisateur
        self.cadre_canal = tk.Frame(self)
        self.cadre_canal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.cadre_message = tk.Frame(self)
        self.cadre_message.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.etiquette_liste_canal = tk.Label(self.cadre_canal, text="Liste des canaux")
        self.etiquette_liste_canal.pack()

        self.liste_canal = tk.Listbox(self.cadre_canal, width=30)
        self.liste_canal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.bouton_actualiser = tk.Button(self.cadre_canal, text="Actualiser", command=self.rafraichir_canaux)
        self.bouton_actualiser.pack()

        self.bouton_creer_canal = tk.Button(self.cadre_canal, text="Créer un canal", command=self.creer_fenetre_canal)
        self.bouton_creer_canal.pack()

        self.bouton_supprimer_canal = tk.Button(self.cadre_canal, text="Supprimer un canal")
        self.bouton_supprimer_canal.pack()

        self.bouton_modifier_canal = tk.Button(self.cadre_canal, text="Modifier un canal")
        self.bouton_modifier_canal.pack()

        self.bouton_rejoindre_canal = tk.Button(self.cadre_canal, text="Rejoindre un canal")
        self.bouton_rejoindre_canal.pack()

        self.bouton_quitter_canal = tk.Button(self.cadre_canal, text="Quitter un canal")
        self.bouton_quitter_canal.pack()

        # self.bouton_supprimer_message = tk.Button(self.cadre_message, text="Supprimer un message")
        # self.bouton_supprimer_message.pack()

        # self.bouton_modifier_message = tk.Button(self.cadre_message, text="Modifier un message")
        # self.bouton_modifier_message.pack()

        self.bouton_actualiser_message = tk.Button(self.cadre_message, text="Actualiser les messages")
        self.bouton_actualiser_message.pack()

        self.etiquette_message = tk.Label(self.cadre_message, text="Message")
        self.etiquette_message.pack()

        self.saisie_message = tk.Entry(self.cadre_message)
        self.saisie_message.pack()
        
        self.bouton_envoyer_message = tk.Button(self.cadre_message, text="Envoyer un message")
        self.bouton_envoyer_message.pack()

        self.etiquette_liste_message = tk.Label(self.cadre_message, text="Messages du canal")
        self.etiquette_liste_message.pack()

        self.liste_message = tk.Listbox(self.cadre_message, width=50)
        self.liste_message.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Chargement initial des canaux
        self.rafraichir_canaux()

    def rafraichir_canaux(self):
        # Efface la liste actuelle des canaux
        self.liste_canal.delete(0, tk.END)

        # Récupère les canaux depuis la base de données
        self.curseur.execute("SELECT name FROM channels")
        canaux = self.curseur.fetchall()

        # Affiche les canaux dans la liste
        for canal in canaux:
            self.liste_canal.insert(tk.END, canal[0])

    def creer_fenetre_canal(self):
        # Fenêtre pour saisir le nom et le type du canal
        fenetre_creation_canal = tk.Toplevel(self)
        fenetre_creation_canal.title("Créer un canal")
        fenetre_creation_canal.geometry("300x200")

        etiquette_nom_canal = tk.Label(fenetre_creation_canal, text="Nom du canal:")
        etiquette_nom_canal.pack()

        saisie_nom_canal = tk.Entry(fenetre_creation_canal)
        saisie_nom_canal.pack()

        etiquette_type_canal = tk.Label(fenetre_creation_canal, text="Type du canal (public/privé):")
        etiquette_type_canal.pack()

        saisie_type_canal = tk.Entry(fenetre_creation_canal)
        saisie_type_canal.pack()

        def enregistrer_canal():
            nom = saisie_nom_canal.get()
            type_c = saisie_type_canal.get()

            # Insertion du nouveau canal dans la base de données
            self.curseur.execute("INSERT INTO channels (name, type, messages) VALUES (%s, %s, %s)", (nom, type_c, ''))
            self.connexion.commit()
            fenetre_creation_canal.destroy()
            self.rafraichir_canaux()

        bouton_enregistrer = tk.Button(fenetre_creation_canal, text="Enregistrer", command=enregistrer_canal)
        bouton_enregistrer.pack() 

if __name__ == "__main__":
    app = GestionnaireCanaux()
    app.mainloop()