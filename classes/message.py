import tkinter as tk
import mysql.connector
from channel import GestionnaireCanaux

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


    # def rafraichir_messages(self):
    #     self.message_listbox.delete(0, tk.END)
    #     messages = self.recupere_messages()
    #     for user_name, content in messages:
    #         self.message_listbox.insert(tk.END, f"{user_name}: {content}")

    def recupere_messages(self):
        self.cursor.execute("SELECT author_id, content FROM messages")
        return self.cursor.fetchall()
    
    def envoyer_message(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydiscord"
        )
        self.cursor = self.conn.cursor()
        canal = GestionnaireCanaux()
        msg = MessageManager
        message = canal.saisie_message.get()
        author_id_query = "SELECT first_name FROM users WHERE email = %s"
        self.cursor.execute(author_id_query, (self.email_utilisateur_actuel,))
        author_id = self.cursor.fetchone()[0]  # Assuming it returns one row

        print(message)
        canal.saisie_message.delete(0, tk.END)
        insert_query = "INSERT INTO messages (author_id, content) VALUES (%s, %s)"
        self.cursor.execute(insert_query, (author_id, message,))
        self.conn.commit()
        msg.rafraichir_messages()
        canal.bouton_envoyer_message.invoke()

    def envoyer_message1(self):
        message = self.message_entry.get()
        author_id = (f"SELECT first_name FROM users WHERE email = %s")
        print(message)
        self.message_entry.delete(0, tk.END)
        self.cursor.execute(f"INSERT INTO messages (author_id, content) VALUES (1, '{message}')")
        self.conn.commit()
        self.rafraichir_messages()
        self.send_button


if __name__ == "__main__":
    app = MessageManager()
    app.mainloop()
