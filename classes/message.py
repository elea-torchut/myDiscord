import tkinter as tk
import mysql.connector


class MessageManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des messages Discord")
        self.geometry("800x600")

        # Connexion à la base de données MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydiscord"
        )
        self.cursor = self.conn.cursor()
        
        # Interface utilisateur pour les messages
        self.message_frame = tk.Frame(self)
        self.message_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.message_list_label = tk.Label(self.message_frame, text="Messages du canal")
        self.message_list_label.pack()
        
        self.message_listbox = tk.Listbox(self.message_frame, width=50)
        self.message_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.rafraichir_messages()

        # Interface utilisateur pour la saisie de messages
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.message_entry = tk.Entry(self.entry_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.send_button = tk.Button(self.entry_frame, text="Envoyer",command=self.envoyer_message)
        self.send_button.pack(side=tk.RIGHT)

        # Bouton pour revenir au menu principal
        self.return_button = tk.Button(self, text="Revenir au menu principal", command=self.destroy)
        self.return_button.pack(anchor=tk.NE)

    def rafraichir_messages(self):
        # Efface tous les messages actuellement affichés
        self.message_listbox.delete(0, tk.END)

        # Récupère une nouvelle liste de messages
        messages = self.recupere_messages()

        # Insère chaque message dans message_listbox
        for user_name, content in messages:
            message_text = f"{user_name}: {content}"
            self.message_listbox.insert(tk.END, message_text)


    def recupere_messages(self):
        self.cursor.execute("SELECT author_id, content FROM messages")
        return self.cursor.fetchall()
    
    def envoyer_message(self):
        try:
            # Connexion à la base de données MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="mydiscord"
            )
            cursor = conn.cursor()

            # Récupération de l'ID de l'auteur du message
            author_id_query = "SELECT id FROM users WHERE email = %s"
            cursor.execute(author_id_query, (self.email_utilisateur_actuel,))
            author_id = cursor.fetchone()[0]
            
            # Récupération du nom de l'utilisateur actuel
            user_name_query = "SELECT first_name FROM users WHERE email = %s"
            cursor.execute(user_name_query, (self.email_utilisateur_actuel,))
            user_name = cursor.fetchone()[0]
            print(user_name)
            

            # Récupération de l'ID du canal actuel
            channel_id_query = "SELECT id FROM channels WHERE name = %s"
            cursor.execute(channel_id_query, (self.nom_canal_actuel,))
            channel_id = cursor.fetchone()[0]

            # Récupération du message depuis l'entrée utilisateur
            message = self.message_entry.get()

            # Insertion du message dans la base de données
            insert_query = "INSERT INTO messages (author_id, channel_id, content) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (author_id, channel_id, message))
            conn.commit()

            # Rafraîchissement des messages dans le gestionnaire de messages
            self.rafraichir_messages()

            # Nettoyage de l'entrée utilisateur après l'envoi
            self.message_entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            print("Erreur lors de l'envoi du message :", err)

        finally:
            # Fermeture du curseur et de la connexion à la base de données
            cursor.close()
            conn.close()


    def envoyer_message(self):
        message = self.message_entry.get()
        # author_name = (f"SELECT first_name FROM users WHERE email = %s")
        print(message)
        self.message_entry.delete(0, tk.END)
        self.cursor.execute(f"INSERT INTO messages (author_id, content) VALUES (1, '{message}')")
        self.conn.commit()
        self.rafraichir_messages()
        self.send_button


if __name__ == "__main__":
    app = MessageManager()
    app.mainloop()
