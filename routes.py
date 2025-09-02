
from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Post
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'isAdmin': user.isAdmin,
            'temporaryPassword': user.temporaryPassword
        }), 200
    return jsonify({'message': 'Credenciais inválidas'}), 401

@bp.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'isAdmin': user.isAdmin,
            'temporaryPassword': user.temporaryPassword
        })
    return jsonify(users_data), 200

@bp.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    isAdmin = data.get('isAdmin', False)

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Nome de usuário já existe'}), 409

    hashed_password = generate_password_hash(password).decode('utf-8')  # Hash and decode to string
    new_user = User(username=username, password=hashed_password, name=name, isAdmin=isAdmin)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário adicionado com sucesso'}), 201

@bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    user.name = data.get('name', user.name)
    user.username = data.get('username', user.username)
    user.isAdmin = data.get('isAdmin', user.isAdmin)
    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso'}), 200

@bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário excluído com sucesso'}), 200

@bp.route('/api/change_password/<int:user_id>', methods=['PUT'])
def change_password(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    if not check_password_hash(user.password, current_password):
        return jsonify({'message': 'Senha atual incorreta'}), 401

    user.password = generate_password_hash(new_password).decode('utf-8')  # Hash and decode to string
    user.temporaryPassword = False
    db.session.commit()
    return jsonify({'message': 'Senha alterada com sucesso'}), 200

@bp.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'problem': post.problem,
            'solution': post.solution,
            'author': post.author,
            'authorId': post.authorId,
            'date': post.date
        })
    return jsonify(posts_data), 200

@bp.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('title')
    problem = data.get('problem')
    solution = data.get('solution')
    author = data.get('author')
    authorId = data.get('authorId')
    date = data.get('date')

    new_post = Post(title=title, problem=problem, solution=solution, author=author, authorId=authorId, date=date)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Postagem adicionada com sucesso'}), 201

@bp.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Postagem excluída com sucesso'}), 200


