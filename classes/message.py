import tkinter as tk
import mysql.connector


class MessageManager(tk.Tk):
    def __init__(self, user_email, nom_canal):
        super().__init__()
        self.title("Gestion des messages Discord")
        self.geometry("800x600")
        self.user_email = user_email
        self.nom_canal = nom_canal

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

        self.canal_label = tk.Label(self.message_frame, text=f"Canal: {self.nom_canal}")
        self.canal_label.pack()


        # self.canal_label = tk.Label(self.message_frame, text=f"Canal: {self.nom_canal}")
        # self.canal_label.pack() 
        
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
        self.message_listbox.delete(0, tk.END)
        messages = self.recupere_messages()
        for user_name, content in messages:
            message_text = f"{user_name}: {content}"
            self.message_listbox.insert(tk.END, message_text)


    def recupere_messages(self):
        # Cette requête SQL joint les tables users et messages pour récupérer le prénom de l'utilisateur et le contenu de chaque message.
        # Assurez-vous que 'self.nom_canal' est correctement défini et correspond au nom du canal actuel.
        query = """
            SELECT u.first_name, m.content
            FROM messages m
            INNER JOIN users u ON m.author_id = u.id
            INNER JOIN channels c ON m.channel_id = c.id
            WHERE c.name = %s
        """
        self.cursor.execute(query, (self.nom_canal,))
        return self.cursor.fetchall()

    
    def envoyer_message(self):
        message = self.message_entry.get().strip()
        if message:  # Assurez-vous que le message n'est pas vide
            try:
                # Utilisez self.conn et self.cursor pour utiliser la connexion existante
                self.cursor.execute("SELECT id FROM users WHERE email = %s", (self.user_email,))
                author_id = self.cursor.fetchone()[0]

                self.cursor.execute("SELECT id FROM channels WHERE name = %s", (self.nom_canal,))
                channel_id = self.cursor.fetchone()[0]

                self.cursor.execute("INSERT INTO messages (author_id, channel_id, content) VALUES (%s, %s, %s)", (author_id, channel_id, message))
                self.conn.commit()

                self.rafraichir_messages()
                self.message_entry.delete(0, tk.END)
            except mysql.connector.Error as err:
                print("Erreur lors de l'envoi du message :", err)



if __name__ == "__main__":
    app = MessageManager()
    app.mainloop()
