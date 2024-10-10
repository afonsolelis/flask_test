from flask import Flask, jsonify, request
from models import User, db
from auth import token_required, generate_token
from database import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

    init_db(app)

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        new_user = User(username=data['username'])
        new_user.set_password(data['password'])  # Usar método set_password
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'})


    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            token = generate_token(user)
            return jsonify({'token': token})
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/users', methods=['GET'])
    @token_required
    def get_users(current_user):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @app.route('/user/<int:id>', methods=['PUT'])
    @token_required
    def update_user(current_user, id):
        data = request.get_json()
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user.username = data.get('username', user.username)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    @app.route('/user/<int:id>', methods=['DELETE'])
    @token_required
    def delete_user(current_user, id):
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
