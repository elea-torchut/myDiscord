import tkinter as tk
import mysql.connector

class ChannelManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des canaux Discord")
        self.geometry("800x600")

        

        # Connexion à la base de données MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123soleil",
            database="mydiscord"
        )
        self.cursor = self.conn.cursor()
        
        # Interface utilisateur
        self.channel_frame = tk.Frame(self)
        self.channel_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.message_frame = tk.Frame(self)
        self.message_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.channel_list_label = tk.Label(self.channel_frame, text="Liste des canaux")
        self.channel_list_label.pack()

        self.channel_listbox = tk.Listbox(self.channel_frame, width=30)
        self.channel_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.refresh_button = tk.Button(self.channel_frame, text="Actualiser", command=self.refresh_channels)
        self.refresh_button.pack()

        self.create_channel_button = tk.Button(self.channel_frame, text="Créer un canal", command=self.create_channel_window)
        self.create_channel_button.pack()

        self.message_list_label = tk.Label(self.message_frame, text="Messages du canal")
        self.message_list_label.pack()

        self.message_listbox = tk.Listbox(self.message_frame, width=50)
        self.message_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        # Chargement initial des canaux
        self.refresh_channels()

    def refresh_channels(self):
        # Efface la liste actuelle des canaux
        self.channel_listbox.delete(0, tk.END)

        # Récupère les canaux depuis la base de données
        self.cursor.execute("SELECT name FROM channels")
        channels = self.cursor.fetchall()

        # Affiche les canaux dans la liste
        for channel in channels:
            self.channel_listbox.insert(tk.END, channel[0])

    def create_channel_window(self):
        # Fenêtre pour saisir le nom et le type du canal
        create_channel_window = tk.Toplevel(self)
        create_channel_window.title("Créer un canal")
        create_channel_window.geometry("300x200")

        name_label = tk.Label(create_channel_window, text="Nom du canal:")
        name_label.pack()

        name_entry = tk.Entry(create_channel_window)
        name_entry.pack()

        type_label = tk.Label(create_channel_window, text="Type du canal (public/privé):")
        type_label.pack()

        type_entry = tk.Entry(create_channel_window)
        type_entry.pack()

        def save_channel():
            name = name_entry.get()
            channel_type = type_entry.get()

            # Insertion du nouveau canal dans la base de données
            self.cursor.execute("INSERT INTO channels (name, type) VALUES (%s, %s)", (name, channel_type))
            self.conn.commit()
            create_channel_window.destroy()
            self.refresh_channels()

        save_button = tk.Button(create_channel_window, text="Enregistrer", command=save_channel)
        save_button.pack()


    # def load_messages(self):
    # # Efface la liste actuelle des messages
    #     self.message_listbox.delete(0, tk.END)

    # # Charge les messages du canal sélectionné depuis la base de données
    #     selected_channel = self.channel_listbox.get(tk.ACTIVE)
    #     self.cursor.execute("SELECT message FROM messages WHERE channel=%s", (selected_channel,))
    #     messages = self.cursor.fetchall()

    # # Affiche les messages dans la liste
    #     for message in messages:
    #         self.message_listbox.insert(tk.END, message[0])


    def send_message(self, channel):
        # Enregistrer le message dans la base de données
        self.cursor.execute("INSERT INTO messages (channel, message) VALUES (%s, %s)", (channel))
        self.conn.commit()

    def receive_messages(self, channel):
        # Récupérer les messages du canal depuis la base de données
        self.cursor.execute("SELECT message FROM messages WHERE channel=%s", (channel))
        messages = self.cursor.fetchall()
        return [message[0] for message in messages]

if __name__ == "__main__":
    app = ChannelManager()
    app.mainloop()
