# main.py
from chatapplication import ChatApplication
from user import Utilisateur
from channel import ChannelManager
from message import MessageManager

# Créer une instance de l'application de chat
app = ChatApplication()

# Créer une instance de la gestion des utilisateurs
user_manager = Utilisateur()

# Créer une instance de la gestion des canaux
channel_manager = ChannelManager()

# Créer une instance de la gestion des messages
message_manager = MessageManager()

# Lancer l'application de chat
app.mainloop()
