#chatapplication.py

import tkinter as tk
import mysql.connector
from channel import ChannelManager

class ChatApplication(tk.Tk):
    # Classe principale pour l'application de chat
    def __init__(self):
        super().__init__()

        # Calcul des dimensions de la fenêtre
        window_width = 800
        window_height = 600

        # Obtention des dimensions de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcul des coordonnées pour centrer la fenêtre
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Configuration de la taille et de la position de la fenêtre
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.title("Chat Discord")

        # Cadre principal pour contenir les éléments
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Titre à l'intérieur de la fenêtre
        title_label = tk.Label(main_frame, text="Bienvenue sur Chat Discord", font=("Arial", 20))
        title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=(175,10))

        # Création des labels et des champs de saisie pour les informations de connexion
        self.label_email = tk.Label(main_frame, text="Email:")
        self.entry_email = tk.Entry(main_frame, width=50)
        
        self.label_prenom = tk.Label(main_frame, text="Prénom:")
        self.entry_prenom = tk.Entry(main_frame, width=50)

        self.label_nom = tk.Label(main_frame, text="Nom:")
        self.entry_nom = tk.Entry(main_frame, width=50)

        self.label_mot_de_passe = tk.Label(main_frame, text="Mot de passe:")
        self.entry_mot_de_passe = tk.Entry(main_frame, show="*", width=50)

        # Création des boutons de connexion et d'inscription
        self.button_connexion = tk.Button(main_frame, text="Se connecter", command=self.connexion_utilisateur, width=20)
        self.button_inscription = tk.Button(main_frame, text="S'inscrire", command=self.inscrire_utilisateur, width=20)

        # Placement des widgets dans le cadre principal
        self.label_email.grid(row=0, column=0, pady=(200,10), padx=150)
        self.entry_email.grid(row=0, column=1, pady=(200,10))
        
        self.label_prenom.grid(row=1, column=0, pady=10)
        self.entry_prenom.grid(row=1, column=1, pady=10)

        self.label_nom.grid(row=2, column=0, pady=10)
        self.entry_nom.grid(row=2, column=1, pady=10)

        self.label_mot_de_passe.grid(row=3, column=0, pady=10)
        self.entry_mot_de_passe.grid(row=3, column=1, pady=10)

        self.button_connexion.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_inscription.grid(row=4, column=1, columnspan=2, pady=10)

    # Méthode pour rediriger l'utilisateur vers la fenêtre de discussion
    def rediriger_vers_discussion(self):
        self.destroy() # Fermer la fenêtre actuelle
        channel = ChannelManager() # Créer une nouvelle fenêtre pour le chat
        channel.mainloop() # Lancer la boucle principale de la fenêtre

    # Méthode pour gérer la connexion de l'utilisateur
    def connexion_utilisateur(self):
        email = self.entry_email.get() # Récupérer l'adresse email saisie par l'utilisateur
        mot_de_passe = self.entry_mot_de_passe.get() # Récupérer le mot de passe saisi par l'utilisateur

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


if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
