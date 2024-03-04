import tkinter as tk
import mysql.connector

class MessageManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des messages Discord")
        self.geometry("800x600")
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
        
        # Interface utilisateur
        self.message_frame = tk.Frame(self)
        self.message_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.message_frame = tk.Frame(self)
        self.message_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.message_list_label = tk.Label(self.message_frame, text="Messages du canal")
        self.message_list_label.pack()
        self.message_list_label = tk.Label(self.message_frame, text="Messages du canal")
        self.message_list_label.pack()

        self.message_listbox = tk.Listbox(self.message_frame, width=50)
        self.message_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.message_listbox = tk.Listbox(self.message_frame, width=50)
        self.message_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Chargement initial des messages
        self.rafraichir_messages()

    def refresh_messages(self):
        # Efface la liste actuelle des messages
        self.message_listbox.delete(0, tk.END) # Supprime tous les éléments de la liste

        # Récupère les messages depuis la base de données
        messages = self.get_messages() # Récupère les messages depuis la base de données

        # Affiche les messages dans la liste
        for message in messages:
            self.message_listbox.insert(tk.END, message[0]) # Ajoute le message à la fin de la liste

    def get_messages(self):
        # Récupère les messages depuis la base de données
        self.cursor.execute("SELECT content FROM messages") # Exécute la requête SQL
        return self.cursor.fetchall() # Récupère tous les résultats de la requête

if __name__ == "__main__":
    app = MessageManager()
    app.mainloop()
