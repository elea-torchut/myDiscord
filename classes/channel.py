#channel.py

from flask_sqlalchemy import SQLAlchemy

# Initialiser l'extension SQLAlchemy
db = SQLAlchemy()

class ChannelManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
