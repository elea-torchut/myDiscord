#main.py

from chatapplication import ChatApplication
from channel import GestionnaireCanaux
from message import MessageManager

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
    app2 = GestionnaireCanaux()
    app2.mainloop()
    app3 = MessageManager
    app3.mainloop()