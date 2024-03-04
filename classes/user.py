# #user.py

# from flask import Flask, request, jsonify # Importation de la classe Flask pour créer une application web
# from flask_sqlalchemy import SQLAlchemy # Importation de la classe SQLAlchemy pour interagir avec une base de données
# from werkzeug.security import generate_password_hash, check_password_hash   # Importation des fonctions pour hacher et vérifier un mot de passe

# app = Flask(__name__) # Création d'une instance de la classe Flask
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydiscord.db' # Configuration de la base de données
# db = SQLAlchemy(app) # Création d'une instance de la classe SQLAlchemy

# # Création de la classe Utilisateur pour représenter la table users dans la base de données
# class Utilisateur(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # Colonne id de type entier et clé primaire
#     prenom = db.Column(db.String(50), nullable=False) # Colonne first_name de type chaîne de caractères et non nulle
#     nom = db.Column(db.String(50), nullable=False) # Colonne last_name de type chaîne de caractères et non nulle
#     email = db.Column(db.String(100), unique=True, nullable=False) # Colonne email de type chaîne de caractères, unique et non nulle
#     mot_de_passe_hash = db.Column(db.String(100), nullable=False) # Colonne password de type chaîne de caractères et non nulle

#     # Méthode pour hacher le mot de passe de l'utilisateur
#     def definir_mot_de_passe(self, mot_de_passe): 
#         self.mot_de_passe_hash = generate_password_hash(mot_de_passe) # Hacher le mot de passe et l'enregistrer dans la colonne password

#     # Méthode pour vérifier le mot de passe de l'utilisateur
#     def verifier_mot_de_passe(self, mot_de_passe):
#         return check_password_hash(self.mot_de_passe_hash, mot_de_passe) # Vérifier si le mot de passe haché correspond au mot de passe saisi par l'utilisateur


# @app.route('/inscription', methods=['POST']) # Décorateur pour la route /inscription avec la méthode HTTP POST
# def inscription(): # Fonction pour gérer l'inscription d'un nouvel utilisateur
#     data = request.json
#     prenom = data.get('prenom')
#     nom = data.get('nom')
#     email = data.get('email')
#     mot_de_passe = data.get('mot_de_passe')

#     # Vérifier si l'email est déjà utilisé
#     if Utilisateur.query.filter_by(email=email).first():
#         return jsonify({'message': 'Cet email est déjà utilisé'}), 400

#     # Créer un nouvel utilisateur
#     nouvel_utilisateur = Utilisateur(prenom=prenom, nom=nom, email=email)
#     nouvel_utilisateur.definir_mot_de_passe(mot_de_passe)

#     # Enregistrer l'utilisateur dans la base de données
#     db.session.add(nouvel_utilisateur)
#     db.session.commit()

#     return jsonify({'message': 'Inscription réussie'}), 201

# @app.route('/connexion', methods=['POST'])
# def connexion():
#     data = request.json
#     email = data.get('email')
#     mot_de_passe = data.get('mot_de_passe')

#     # Récupérer l'utilisateur depuis la base de données
#     utilisateur = Utilisateur.query.filter_by(email=email).first()

#     if utilisateur and utilisateur.verifier_mot_de_passe(mot_de_passe):
#         return jsonify({'message': 'Connexion réussie'}), 200
#     else:
#         return jsonify({'message': 'Adresse email ou mot de passe invalide'}), 401

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
# from chatapplication import ChatApplication


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
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

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
            password="002003",
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


    # @app.route('/connexion', methods=['POST'])
    # def connexion():
    #     data = request.json
    #     # email = data.get('email')
    #     # mot_de_passe = data.get('password')

    #     # # Connexion à la base de données MySQL
    #     # connection = mysql.connector.connect(
    #     #     host="localhost",
    #     #     user="root",
    #     #     password="root",
    #     #     database="mydiscord"
    #     # )

    #     # cursor = connection.cursor()

    #     # # Récupérer l'utilisateur depuis la base de données
    #     # query = "SELECT * FROM users WHERE email = %s"
    #     # cursor.execute(query, (email,))
    #     # utilisateur = cursor.fetchone()

    #     # if utilisateur and check_password_hash(utilisateur[4], mot_de_passe):
    #     #     query = "UPDATE users SET last_login = NOW() WHERE email = %s"
    #     #     cursor.execute(query, (email,))
    #     #     cursor.close()
    #     #     connection.close()
    #     #     return jsonify({'message': 'Connexion réussie'}), 200
    #     # else:
    #     #     cursor.close()
    #     #     connection.close()
    #     #     return jsonify({'message': 'Adresse email ou mot de passe invalide'}), 401
        
    #     email = self.entry_email.get()
    #     mot_de_passe = self.entry_mot_de_passe.get()

    #     # Connexion à la base de données MySQL
    #     connection = mysql.connector.connect(
    #         host="localhost",
    #         user="root",
    #         password="root",
    #         database="mydiscord"
    #     )

    #     cursor = connection.cursor()

    #     # Vérification des informations de connexion dans la base de données
    #     query = "SELECT * FROM users WHERE email = %s"
    #     cursor.execute(query, (email,))
    #     utilisateur = cursor.fetchone()

    #     if utilisateur and utilisateur[4] == mot_de_passe:
    #         print("Connexion réussie")
    #         self.rediriger_vers_discussion()
    #     else:
    #         print("Adresse email ou mot de passe invalide")

    #     # Fermeture du curseur et de la connexion
    #     cursor.close()
    #     connection.close()


    @app.route('/deconnexion', methods=['POST'])
    def deconnexion_utilisateur(self):
        # Vous pouvez ajouter ici toute logique de nettoyage ou de traitement de déconnexion nécessaire

        # Par exemple, si vous avez une session ouverte, vous pouvez la fermer
        self.fermer_session()

        # Vous pouvez également rediriger l'utilisateur vers une page de déconnexion ou une autre page d'accueil
        self.rediriger_vers_page_accueil_apres_deconnexion()

    def fermer_session(self):
        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="002003",
            database="mydiscord"
        )

        cursor = connection.cursor()
        
        # Exécuter une requête SQL pour mettre à jour la date de dernière déconnexion de l'utilisateur
        query = "UPDATE users SET last_logout = NOW() WHERE email = %s"
        cursor.execute(query, (self.email,))
        connection.commit()

        # Fermeture du curseur et de la connexion
        cursor.close()
        connection.close()

    def rediriger_vers_page_accueil_apres_deconnexion(self):
        app = ChatApplication()
        app.mainloop()
    
    # @app.route('/deconnexion', methods=['POST'])
    # def deconnexion(self):
    #     data = request.json
    #     email = data.get('email')
    #     mot_de_passe = data.get('password')

        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="002003",
            database="mydiscord"
        )

    #     cursor = connection.cursor()

    #     query = "UPDATE users SET last_logout = NOW() WHERE email = %s"
    #     cursor.execute(query, (email,))
    #     cursor.close()
    #     connection.close()
    #     return jsonify({'message': 'Déconnexion réussie'}), 200

if __name__ == '__main__':
    app.run(debug=True)

