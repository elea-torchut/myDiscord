import tkinter as tk
from tkinter import messagebox
import requests

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("My Discord - Connexion")

        self.email_label = tk.Label(root, text="Email:")
        self.email_entry = tk.Entry(root)
        self.email_label.grid(row=0, column=0, sticky="e")
        self.email_entry.grid(row=0, column=1)

        self.password_label = tk.Label(root, text="Mot de passe:")
        self.password_entry = tk.Entry(root, show="*")
        self.password_label.grid(row=1, column=0, sticky="e")
        self.password_entry.grid(row=1, column=1)

        self.connect_button = tk.Button(root, text="Se connecter", command=self.login)
        self.connect_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(root, text="S'inscrire", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Envoyer les informations de connexion au serveur pour vérification
        # Vous devez implémenter cette partie en fonction de votre serveur
        # Par exemple, vous pouvez utiliser une requête HTTP POST pour envoyer les informations

    def register(self):
        # Ouvrir une nouvelle fenêtre pour l'inscription
        register_window = tk.Toplevel(self.root)
        register_window.title("Inscription")

        # Ajouter les champs pour l'inscription
        # Vous pouvez utiliser une mise en page similaire à celle de la fenêtre de connexion

        # Ajouter un bouton pour enregistrer le nouvel utilisateur
        register_button = tk.Button(register_window, text="S'inscrire", command=self.save_user)
        register_button.pack()

    #def save_user(self):
        # Récupérer les informations saisies par l'utilisateur dans la fenêtre d'inscription
        # Envoyer les informations au serveur pour enregistrer le nouvel utilisateur
        # Vous devez implémenter cette partie en fonction de votre serveur

        # Fermer la fenêtre d'inscription après l'enregistrement
        # Vous pouvez utiliser register_window.destroy() pour fermer la fenêtre


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
