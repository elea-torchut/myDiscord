#user.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialiser l'extension SQLAlchemy
db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(100), nullable=False)

    def definir_mot_de_passe(self, mot_de_passe):
        """
        Permet de définir le mot de passe de l'utilisateur de manière sécurisée.
        """
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def verifier_mot_de_passe(self, mot_de_passe):
        """
        Vérifie si le mot de passe donné correspond au mot de passe de l'utilisateur.
        """
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

    @classmethod
    def inscription(cls, prenom, nom, email, mot_de_passe):
        """
        Enregistre un nouvel utilisateur dans la base de données.
        """
        utilisateur = cls(prenom=prenom, nom=nom, email=email)
        utilisateur.definir_mot_de_passe(mot_de_passe)
        db.session.add(utilisateur)
        db.session.commit()
        return utilisateur

    @classmethod
    def connexion(cls, email, mot_de_passe):
        """
        Permet à un utilisateur de se connecter.
        """
        utilisateur = cls.query.filter_by(email=email).first()
        if utilisateur and utilisateur.verifier_mot_de_passe(mot_de_passe):
            return utilisateur
        return None

    def deconnexion(self):
        """
        Permet à l'utilisateur de se déconnecter (dans ce cas, une fonction factice).
        """
        # Vous pouvez implémenter des fonctionnalités de déconnexion si nécessaire
        pass

    def mettre_a_jour_informations(self, prenom=None, nom=None, email=None):
        """
        Met à jour les informations personnelles de l'utilisateur.
        """
        if prenom:
            self.prenom = prenom
        if nom:
            self.nom = nom
        if email:
            self.email = email
        db.session.commit()

