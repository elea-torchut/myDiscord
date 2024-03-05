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
            password="002003",
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
        self.send_button = tk.Button(self.entry_frame, text="Envoyer")
        self.send_button.pack(side=tk.RIGHT)

        # Bouton pour revenir au menu principal
        self.return_button = tk.Button(self, text="Revenir au menu principal", command=self.destroy)
        self.return_button.pack(anchor=tk.NE)

    def rafraichir_messages(self):
        self.message_listbox.delete(0, tk.END)
        messages = self.recupere_messages()
        for user_name, content in messages:
            self.message_listbox.insert(tk.END, f"{user_name}: {content}")

    def recupere_messages(self):
        self.cursor.execute("SELECT author_id, content FROM messages")
        return self.cursor.fetchall()
    
    def envoyer_message(self): 
        message = self.saisie_message.get() # Récupère le message saisi par l'utilisateur
        print(message)
        self.etiquette_liste_message # Affiche le message dans l'interface utilisateur

        self.curseur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        self.connexion.commit() # Enregistre le message dans la base de données


        message = MessageManager() # Crée une instance de la classe MessageManager
        message = self.saisie_message.get() # Récupère le message saisi par l'utilisateur
        self.curseur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        self.connexion.commit()
    

if __name__ == "__main__":
    app = MessageManager()
    app.mainloop()
