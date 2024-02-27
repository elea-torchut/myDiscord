# user.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

# Initialiser l'application Flask
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/mydiscord'
db = SQLAlchemy(app)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(100), nullable=False)

    def definir_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe) # Génère un hash du mot de passe

    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe) # Retourne True si le mot de passe est correct

@app.route('/inscription', methods=['POST'])
def inscription():
    data = request.json
    prenom = data.get('first_name')
    nom = data.get('last_name')
    email = data.get('email')
    mot_de_passe = data.get('password')

    # Connexion à la base de données MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mydiscord"
    )

    cursor = connection.cursor()

    # Vérifier si l'email est déjà utilisé
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    utilisateur = cursor.fetchone()

    if utilisateur:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Cet email est déjà utilisé'}), 400

    # Créer un nouvel utilisateur
    nouvel_utilisateur = Utilisateur(prenom=prenom, nom=nom, email=email)
    nouvel_utilisateur.definir_mot_de_passe(mot_de_passe)

    # Insertion d'un nouvel utilisateur dans la base de données
    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (prenom, nom, email, nouvel_utilisateur.mot_de_passe_hash))
    connection.commit()

    # Fermeture du curseur et de la connexion
    cursor.close()
    connection.close()

    return jsonify({'message': 'Inscription réussie'}), 201


@app.route('/connexion', methods=['POST'])
def connexion():
    data = request.json
    email = data.get('email')
    mot_de_passe = data.get('password')

    # Connexion à la base de données MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mydiscord"
    )

    cursor = connection.cursor()

    # Récupérer l'utilisateur depuis la base de données
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    utilisateur = cursor.fetchone()

    if utilisateur and check_password_hash(utilisateur[4], mot_de_passe):
        query = "UPDATE users SET last_login = NOW() WHERE email = %s"
        cursor.execute(query, (email,))
        cursor.close()
        connection.close()
        return jsonify({'message': 'Connexion réussie'}), 200
    else:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Adresse email ou mot de passe invalide'}), 401

if __name__ == '__main__':
    app.run(debug=True)
