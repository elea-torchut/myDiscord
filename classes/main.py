# main.py
from chatapplication import ChatApplication
from message import MessageManager
from server import app as server_app
from user import Utilisateur, app as user_app

if __name__ == "__main__":
    # Créer une instance de l'application de chat
    chat_app = ChatApplication()

    # Créer une instance du gestionnaire de messages
    message_manager = MessageManager()

    # Exécuter le serveur Flask pour les utilisateurs
    user_app.run(debug=True)

    # Exécuter le serveur Flask pour le chat
    server_app.run(debug=True)
