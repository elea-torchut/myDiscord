from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, request, jsonify
from user import db as user_db, User
from message import db as message_db, Message
from channel import db as channel_db, Channel

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/mydiscord'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser l'extension SQLAlchemy pour le modèle User
user_db.init_app(app)
# Initialiser l'extension SQLAlchemy pour le modèle Message
message_db.init_app(app)
# Initialiser l'extension SQLAlchemy pour le modèle Channel
channel_db.init_app(app)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=data['password'])
    user_db.session.add(new_user)
    user_db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        result.append(user_data)
    return jsonify(result), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    return jsonify(user_data), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.password = data['password']
    user_db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user_db.session.delete(user)
    user_db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
