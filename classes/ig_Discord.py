# # discord.py
# import tkinter as tk
# import requests

# # Fonction pour charger les utilisateurs depuis le serveur backend
# def load_users():
#     # Faire une requête GET au serveur backend pour récupérer les utilisateurs

#     url = "http://localhost:3306/mydiscord/users"  # Remplacez l'URL par celle de votre serveur backend
#     try:
#         response = requests.get(url) # Faire une requête GET au serveur backend pour récupérer les utilisateurs
#         if response.status_code == 200: # Vérifier si la requête a réussi (code 200)
#             users = response.json() # Convertir la réponse JSON en liste d'utilisateurs
#             for user in users: # Parcourir la liste des utilisateurs
#                 user_listbox.insert(tk.END, f"{user['first_name']} {user['last_name']} - {user['email']}") # Ajouter chaque utilisateur à la liste des utilisateurs
#         else:
#             print("Erreur lors de la requête:", response.status_code) # Afficher le code d'erreur dans la console 
#             # Afficher un message d'erreur dans la liste des utilisateurs
#             user_listbox.insert(tk.END, "Failed to load users") # Afficher un message d'erreur dans la liste des utilisateurs
#     except requests.exceptions.RequestException as e: # Gérer les erreurs de connexion au serveur backend
#         print("Erreur de connexion:", e) # Afficher l'erreur dans la console 
#         # Afficher un message d'erreur dans la liste des utilisateurs
#         user_listbox.insert(tk.END, "Failed to connect to the server") # Afficher un message d'erreur dans la liste des utilisateurs

# # Créer la fenêtre principale
# root = tk.Tk() # Créer une fenêtre principale
# root.title("My Discord") # Définir le titre de la fenêtre

# # Créer un cadre pour les utilisateurs
# user_frame = tk.Frame(root) # Créer un cadre pour les utilisateurs
# user_frame.pack(padx=10, pady=10) # Ajouter le cadre à la fenêtre principale

# # Créer une liste pour afficher les utilisateurs
# user_listbox = tk.Listbox(user_frame, width=80, height=20) # Créer une liste pour afficher les utilisateurs
# user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Ajouter la liste au cadre

# # Créer une barre de défilement pour la liste des utilisateurs
# scrollbar = tk.Scrollbar(user_frame) # Créer une barre de défilement pour la liste des utilisateurs
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Ajouter la barre de défilement au cadre
# user_listbox.config(yscrollcommand=scrollbar.set) # Configurer la liste pour utiliser la barre de défilement
# scrollbar.config(command=user_listbox.yview) # Configurer la barre de défilement pour déplacer la liste

# # Charger les utilisateurs depuis le serveur backend
# load_users() # Appeler la fonction pour charger les utilisateurs depuis le serveur backend

# # Ajouter du contenu à la fenêtre
# label = tk.Label(root, text="Liste des utilisateurs de My Discord") # Créer une étiquette pour afficher un message
# label.pack(padx=20, pady=20) # Ajouter l'étiquette à la fenêtre principale

# # Lancer la boucle principale de l'interface graphique
# root.mainloop() # Lancer la boucle principale de l'interface graphique
