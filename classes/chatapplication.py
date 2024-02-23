import tkinter as tk
import mysql.connector
from channel import ChannelManager

class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chat Discord")

        # Création des labels et des champs de saisie pour les informations de connexion
        self.label_email = tk.Label(self, text="Email:")
        self.entry_email = tk.Entry(self)
        
        self.label_prenom = tk.Label(self, text="Prénom:")
        self.entry_prenom = tk.Entry(self)

        self.label_nom = tk.Label(self, text="Nom:")
        self.entry_nom = tk.Entry(self)

        self.label_mot_de_passe = tk.Label(self, text="Mot de passe:")
        self.entry_mot_de_passe = tk.Entry(self, show="*")

        # Création des boutons de connexion et d'inscription
        self.button_connexion = tk.Button(self, text="Se connecter", command=self.connexion_utilisateur)
        self.button_inscription = tk.Button(self, text="S'inscrire", command=self.inscrire_utilisateur)

        # Placement des widgets dans la fenêtre
        self.label_email.grid(row=0, column=0, sticky="e")
        self.entry_email.grid(row=0, column=1)
        
        self.label_prenom.grid(row=1, column=0, sticky="e")
        self.entry_prenom.grid(row=1, column=1)

        self.label_nom.grid(row=2, column=0, sticky="e")
        self.entry_nom.grid(row=2, column=1)

        self.label_mot_de_passe.grid(row=3, column=0, sticky="e")
        self.entry_mot_de_passe.grid(row=3, column=1)

        self.button_connexion.grid(row=4, column=0, columnspan=2, sticky="we")
        self.button_inscription.grid(row=5, column=0, columnspan=2, sticky="we")

    def rediriger_vers_discussion(self):
        self.destroy()
        channel = ChannelManager()
        channel.mainloop()

    def connexion_utilisateur(self):
        email = self.entry_email.get()
        mot_de_passe = self.entry_mot_de_passe.get()

        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydiscord"
        )

        cursor = connection.cursor()

        # Vérification des informations de connexion dans la base de données
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        utilisateur = cursor.fetchone()

        if utilisateur and utilisateur[4] == mot_de_passe:
            print("Connexion réussie")
            self.rediriger_vers_discussion()
        else:
            print("Adresse email ou mot de passe invalide")

        # Fermeture du curseur et de la connexion
        cursor.close()
        connection.close()

    def inscrire_utilisateur(self):
        prenom = self.entry_prenom.get()
        nom = self.entry_nom.get()
        email = self.entry_email.get()
        mot_de_passe = self.entry_mot_de_passe.get()

        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root", 
            database="mydiscord" 

        )

        cursor = connection.cursor()

        # Insertion d'un nouvel utilisateur dans la base de données
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (prenom, nom, email, mot_de_passe))
        connection.commit()

        print("Inscription réussie")

        # Fermeture du curseur et de la connexion
        cursor.close()
        connection.close()

    def rediriger_vers_discussion(self):
        # Ajoutez ici le code pour ouvrir une nouvelle fenêtre de discussion
        pass

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
