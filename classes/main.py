#main.py

from chatapplication import ChatApplication
from channel import GestionnaireCanaux
from message import MessageManager

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
    if app.connexion_utilisateur:
        app = GestionnaireCanaux(app.utilisateur_actuel)
        app.
        if app.utilisateur_actuel:
            app = MessageManager(app.utilisateur_actuel)
            app.mainloop()

  