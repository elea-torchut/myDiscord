#main.py

from chatapplication import ChatApplication
from channel import GestionnaireCanaux
from message import MessageManager

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()

    if app.connexion_utilisateur():
        canal = GestionnaireCanaux()
        msg = MessageManager()
        canal.mainloop()  
