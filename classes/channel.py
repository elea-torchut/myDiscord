import tkinter as tk
import mysql.connector
from message import MessageManager

class GestionnaireCanaux(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des canaux Discord")
        self.geometry("800x600")
        self.utilisateur_actuel = None
        self.email_utilisateur_actuel = None

        # Connexion à la base de données MySQL
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="002003",
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

        self.bouton_supprimer_canal = tk.Button(self.cadre_canal, text="Supprimer un canal", command=self.supprimer_canal)
        self.bouton_supprimer_canal.pack()

        self.bouton_modifier_canal = tk.Button(self.cadre_canal, text="Modifier un canal", command=self.modifier_canal)
        self.bouton_modifier_canal.pack()

        self.bouton_rejoindre_canal = tk.Button(self.cadre_canal, text="Rejoindre un canal", command=self.rejoindre_canal) 
        self.bouton_rejoindre_canal.pack()

        self.bouton_quitter_canal = tk.Button(self.cadre_canal, text="Quitter un canal", command=self.quitter_canal)
        self.bouton_quitter_canal.pack()

        self.bouton_actualiser_message = tk.Button(self.cadre_message, text="Actualiser les messages")
        self.bouton_actualiser_message.pack()

        self.etiquette_message = tk.Label(self.cadre_message, text="Message")
        self.etiquette_message.pack()

        self.saisie_message = tk.Entry(self.cadre_message)
        self.saisie_message.pack()
        
        self.bouton_envoyer_message = tk.Button(self.cadre_message, text="Envoyer un message", command=self.envoyer_message)
        self.bouton_envoyer_message.pack()

        self.etiquette_liste_message = tk.Label(self.cadre_message, text="Messages du canal")
        self.etiquette_liste_message.pack()

        self.liste_message = tk.Listbox(self.cadre_message, width=50)
        self.liste_message.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.bouton_deconnexion = tk.Button(self.cadre_message, text="Se déconnecter", command=self.deconnexion_utilisateur)
        self.bouton_deconnexion.pack()

        # Création de la combobox pour afficher les canaux disponibles
        self.label_liste_canal = tk.Label(self.cadre_canal, text="Liste des canaux disponibles")
        self.label_liste_canal.pack()

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

            # Ajoutez le bouton de modification de canal dans la méthode __init__
            self.bouton_modifier_canal = tk.Button(self.cadre_canal, text="Modifier un canal", command=self.modifier_canal)
            self.bouton_modifier_canal.pack()

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
                # Insérer une nouvelle entrée dans la table channel_members
                self.curseur.execute("INSERT INTO channel_members (channel_id, user_id) VALUES (%s, %s)", (channel_id, self.utilisateur_actuel))
                self.connexion.commit()
                print(f"L'utilisateur {self.utilisateur_actuel} a rejoint le canal {nom_canal} avec succès.")
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


    # def rejoindre_canal(self):
    #     # Récupérer le nom du canal sélectionné dans la liste
    #     nom_canal = self.liste_canal.get(tk.ACTIVE)

    #     # Récupérer l'ID de l'utilisateur actuel à partir de votre gestionnaire de canaux
    #     id_utilisateur = self.utilisateur_actuel  # Assurez-vous que cela contient l'ID de l'utilisateur actuel

    #     # Mettre à jour la colonne "liste_utilisateurs" dans la table "channels"
    #     try:
    #         self.curseur.execute("UPDATE channels SET liste_utilisateurs = CONCAT(liste_utilisateurs, ', ', %s) WHERE name = %s", (id_utilisateur, nom_canal) )

    #         self.connexion.commit()
    #         print(f"L'utilisateur {id_utilisateur} a rejoint le canal {nom_canal} avec succès.")
    #     except mysql.connector.Error as err:
    #         print("Erreur lors de la mise à jour des utilisateurs dans le canal :", err)


    # def rejoindre_canal(self):
    #     # Récupérer l'indice de l'élément sélectionné dans la liste des canaux
    #     indice_selectionne = self.liste_canal.curselection()
        
    #     # Vérifier si un élément est sélectionné
    #     if indice_selectionne:
    #         # Récupérer le nom du canal à partir de l'indice sélectionné
    #         nom_canal = self.liste_canal.get(indice_selectionne[0])

    #         # Récupérer l'ID de l'utilisateur actuel
    #         id_utilisateur = self.utilisateur_actuel

    #         try:
    #             # Mettre à jour la colonne 'liste_utilisateurs' dans la table 'channels'
    #             self.curseur.execute("UPDATE channels SET liste_utilisateurs = CONCAT(liste_utilisateurs, ', %s') WHERE name = %s", (id_utilisateur, nom_canal))
    #             self.connexion.commit()
    #             print(f"L'utilisateur {id_utilisateur} a rejoint le canal {nom_canal} avec succès.")
    #         except mysql.connector.Error as err:
    #             print("Erreur lors de la mise à jour de la liste des utilisateurs dans le canal :", err)
    #     else:
    #         print("Aucun canal sélectionné.")

    def envoyer_message(self):
        message = self.saisie_message.get()
        print(message)
        self.etiquette_liste_message

        self.curseur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        self.connexion.commit()


        message = MessageManager()
        message = self.saisie_message.get()
        self.curseur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        self.connexion.commit()

        
    # Méthode pour vérifier l'identification de l'utilisateur
    def verifier_identification(self, email, mot_de_passe):
        try:
            self.curseur.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, mot_de_passe))
            utilisateur = self.curseur.fetchone()
            if utilisateur:
                self.utilisateur_actuel = utilisateur[0]
                self.email_utilisateur_actuel = email
                print("Session ouverte pour l'utilisateur avec succès !")
                return True
            else:
                print("Identifiants incorrects.")
                return False
        except mysql.connector.Error as err:
            print("Erreur lors de la vérification de l'identification :", err)
            return False

    
    def deconnexion_utilisateur(self):
        # Vous pouvez ajouter ici toute logique de nettoyage ou de traitement de déconnexion nécessaire

        # Par exemple, si vous avez une session ouverte, vous pouvez la fermer
        self.fermer_session()

        # Vous pouvez également rediriger l'utilisateur vers une page de déconnexion ou une autre page d'accueil
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
