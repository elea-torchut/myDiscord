import tkinter as tk
from tkinter import PhotoImage
import mysql.connector
from message import MessageManager

class GestionnaireCanaux(tk.Tk):
    def __init__(self,email_utilisateur_actuel=None):
        super().__init__()
        self.title("Gestion des canaux Discord")
        self.geometry("800x600")
        self.utilisateur_actuel = None
        self.email_utilisateur_actuel = email_utilisateur_actuel


        # Connexion à la base de données MySQL
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydiscord"
        )
        self.curseur = self.connexion.cursor()
        
        # Interface utilisateur
        self.cadre_haut = tk.Frame(self)
        self.cadre_haut.pack(side=tk.TOP, fill=tk.X)

        self.etiquette_utilisateur = tk.Label(self.cadre_haut, text="Utilisateur actuel: Aucun")
        self.etiquette_utilisateur.pack(side=tk.LEFT, padx=10, pady=5)

        self.cadre_canal = tk.Frame(self)
        self.cadre_canal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.cadre_droit = tk.Frame(self)
        self.cadre_droit.pack(side=tk.RIGHT, fill=tk.Y)

        self.etiquette_liste_canal = tk.Label(self.cadre_canal, text="Liste des canaux")
        self.etiquette_liste_canal.pack()

        self.liste_canal = tk.Listbox(self.cadre_canal, width=30)
        self.liste_canal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Création des boutons à l'extrême droite
        self.creer_boutons(self.cadre_droit)

        # Chargement initial des canaux
        self.rafraichir_canaux()

    def creer_boutons(self, cadre):
        # Liste des tuples (texte du bouton, méthode associée)
        actions = [
            ("Actualiser", self.rafraichir_canaux),
            ("Créer un canal", self.creer_fenetre_canal),
            ("Supprimer un canal", self.supprimer_canal),
            ("Modifier un canal", self.modifier_canal),
            ("Rejoindre un canal", self.rejoindre_canal),
            ("Quitter un canal", self.quitter_canal),
            ("Rejoindre canal", self.acceder_a_la_messagerie_du_canal),
            ("Se déconnecter", self.deconnexion_utilisateur)
        ]

        for texte, commande in actions:
            bouton = tk.Button(cadre, text=texte, command=commande)
            bouton.pack(fill=tk.X, pady=2)


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

    def supprimer_canal(self):
        # Récupère le nom du canal sélectionné dans la liste
        nom_canal = self.liste_canal.get(tk.ACTIVE)

        # Exécute la requête SQL pour supprimer le canal de la base de données
        self.curseur.execute("DELETE FROM channels WHERE name = %s", (nom_canal,))
        self.connexion.commit()

        # Rafraîchit la liste des canaux pour refléter les changements
        self.rafraichir_canaux()

    def modifier_canal(self):
        # Récupère le nom du canal sélectionné dans la liste
        nom_canal = self.liste_canal.get(tk.ACTIVE)

        # Crée une fenêtre de modification de canal
        fenetre_modification_canal = tk.Toplevel(self)
        fenetre_modification_canal.title("Modifier le canal")
        fenetre_modification_canal.geometry("300x200")

        # Étiquette pour le nouveau nom du canal
        etiquette_nouveau_nom_canal = tk.Label(fenetre_modification_canal, text="Nouveau nom du canal:")
        etiquette_nouveau_nom_canal.pack()

        # Saisie du nouveau nom du canal
        saisie_nouveau_nom_canal = tk.Entry(fenetre_modification_canal)
        saisie_nouveau_nom_canal.pack()

        # Bouton pour enregistrer les modifications
        bouton_enregistrer_modification = tk.Button(fenetre_modification_canal, text="Enregistrer", command=lambda: enregistrer_modification(saisie_nouveau_nom_canal.get()))
        bouton_enregistrer_modification.pack()

        # Fonction pour enregistrer les modifications
        def enregistrer_modification(nouveau_nom):
            # Exécute la requête SQL pour mettre à jour le nom du canal dans la base de données
            self.curseur.execute("UPDATE channels SET name = %s WHERE name = %s", (nouveau_nom, nom_canal))
            self.connexion.commit()

            # Ferme la fenêtre de modification de canal
            fenetre_modification_canal.destroy()

            # Rafraîchit la liste des canaux pour refléter les changements
            self.rafraichir_canaux()


    def charger_canaux_disponibles(self):
        # Cette méthode charge les canaux disponibles dans la combobox
        try:
            self.curseur.execute("SELECT name FROM channels")
            canaux = self.curseur.fetchall()
            canaux_disponibles = [canal[0] for canal in canaux]
            self.liste_canal["values"] = canaux_disponibles
        except mysql.connector.Error as err:
            print("Erreur lors du chargement des canaux disponibles :", err)

    def rejoindre_canal(self):
        # Récupérer le nom du canal sélectionné dans la liste
        nom_canal = self.liste_canal.get(tk.ACTIVE)

        try:
            # Récupérer l'ID du canal à partir de son nom
            self.curseur.execute("SELECT id FROM channels WHERE name = %s", (nom_canal,))
            resultat = self.curseur.fetchone()
            if resultat:
                channel_id = resultat[0]

                # Vérifier si l'utilisateur est déjà membre du canal
                self.curseur.execute("SELECT * FROM channel_members WHERE channel_id = %s AND user_id = %s", (channel_id, self.utilisateur_actuel))
                if self.curseur.fetchone():
                    print(f"L'utilisateur {self.utilisateur_actuel} est déjà membre du canal {nom_canal}.")
                    return

                # Insérer une nouvelle entrée dans la table channel_members
                self.curseur.execute("INSERT INTO channel_members (channel_id, user_id) VALUES (%s, %s)", (channel_id, self.utilisateur_actuel))
                self.connexion.commit()
                print(f"L'utilisateur {self.utilisateur_actuel} a rejoint le canal {nom_canal} avec succès.")
                print(f"ID du canal : {channel_id}")

            else:
                print("Canal non trouvé.")
        except mysql.connector.Error as err:
            print("Erreur lors de l'ajout de l'utilisateur au canal :", err)


    def quitter_canal(self):
        # Récupérer le nom du canal sélectionné dans la liste
        nom_canal = self.liste_canal.get(tk.ACTIVE)

        try:
            # Récupérer l'ID du canal à partir de son nom
            self.curseur.execute("SELECT id FROM channels WHERE name = %s", (nom_canal,))
            resultat = self.curseur.fetchone()
            if resultat:
                channel_id = resultat[0]
                # Supprimer l'entrée correspondante de la table channel_members
                self.curseur.execute("DELETE FROM channel_members WHERE channel_id = %s AND user_id = %s", (channel_id, self.utilisateur_actuel))
                self.connexion.commit()
                print(f"L'utilisateur {self.utilisateur_actuel} a quitté le canal {nom_canal} avec succès.")
            else:
                print("Canal non trouvé.")
        except mysql.connector.Error as err:
            print("Erreur lors de la suppression de l'utilisateur du canal :", err)

    def acceder_a_la_messagerie_du_canal(self):
        try:
            # Récupérer le nom du canal sélectionné dans la liste
            nom_canal = self.liste_canal.get(tk.ACTIVE)

            # Vérifiez si un canal est sélectionné
            if nom_canal:
                # Créez une nouvelle instance de MessageManager en passant l'email utilisateur et le nom du canal
                fenetre_messages = MessageManager(self.email_utilisateur_actuel, nom_canal)

                # Plus de code pour afficher la fenêtre des messages
                fenetre_messages.mainloop()
            else:
                print("Aucun canal sélectionné.")
        except Exception as e:  # Utilisez Exception as e pour plus de généralité
            print(f"Erreur lors de l'accès à la messagerie du canal: {e}")



    def charger_messages_du_canal(self, canal_id):
        try:
            # Récupérer les messages du canal à partir de son identifiant
            self.curseur.execute("SELECT author_id, content FROM messages WHERE channel_id = %s", (canal_id,))
            messages = self.curseur.fetchall()

            # Insérer chaque message dans la liste des messages
            for author_id, content in messages:
                # Récupérer le nom de l'auteur du message
                self.curseur.execute("SELECT first_name FROM users WHERE id = %s", (author_id,))
                user_name = self.curseur.fetchone()[0]

                # Afficher le message dans la liste des messages
                message_text = f"{user_name}: {content}"
                self.liste_message.insert(tk.END, message_text)
        except mysql.connector.Error as err:
            print("Erreur lors du chargement des messages du canal :", err)

        
    # Méthode pour vérifier l'identification de l'utilisateur
    def verifier_identification(self, email, mot_de_passe):
        try:
            self.curseur.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, mot_de_passe,))
            utilisateur = self.curseur.fetchone()
            if utilisateur:
                print("Identification réussie.")
                self.utilisateur_actuel = utilisateur[0]
                self.email_utilisateur_actuel = email
                self.etiquette_utilisateur["text"] = f"Utilistateur : {email}"
                return True
            else:
                print("Identifiants incorrects.")
                return False
        except mysql.connector.Error as err:
            print("Erreur lors de la vérification de l'identification :", err)
            return False

    # Méthode pour déconnecter l'utilisateur
    def deconnexion_utilisateur(self):
        self.fermer_session()

        # Rediriger l'utilisateur vers la page d'accueil
        self.rediriger_vers_page_accueil_apres_deconnexion()

    def fermer_session(self):
        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydiscord"
        )

        cursor = connection.cursor()
        
        # Exécuter une requête SQL pour mettre à jour la date de dernière déconnexion de l'utilisateur
        query = "UPDATE users SET session_active = 0 WHERE email = %s"
        cursor.execute(query, (self.email_utilisateur_actuel,))
        connection.commit()

        # Fermeture du curseur et de la connexion
        cursor.close()
        connection.close()

    def rediriger_vers_page_accueil_apres_deconnexion(self):
        self.destroy()


if __name__ == "__main__":
    app = GestionnaireCanaux()
    app.mainloop()
