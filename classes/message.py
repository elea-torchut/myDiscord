#message.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialiser l'extension SQLAlchemy
db = SQLAlchemy()

# Créer la classe Message
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Identifiant unique
    contenu = db.Column(db.Text, nullable=False) # Contenu du message
    horodatage = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # Date et heure de création
    id_auteur = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Identifiant de l'auteur
    auteur = db.relationship('User', backref=db.backref('messages', lazy=True)) # Auteur du message
    id_channel = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False) # Identifiant du channel
    channel = db.relationship('Channel', backref=db.backref('messages', lazy=True)) # Channel du message

    
    @staticmethod
    def creer_message(contenu, id_auteur, id_channel):
        nouveau_message = Message(contenu=contenu, id_auteur=id_auteur, id_channel=id_channel)
        db.session.add(nouveau_message)
        db.session.commit()
        return nouveau_message

    @staticmethod
    def obtenir_message_par_id(message_id):
        return Message.query.get(message_id)

    def mettre_a_jour_message(self, nouveau_contenu):
        self.contenu = nouveau_contenu
        db.session.commit()

    def supprimer_message(self):
        db.session.delete(self)
        db.session.commit()
    


