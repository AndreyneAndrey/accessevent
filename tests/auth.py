from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash



auth = Blueprint('auth', __name__)

@auth.route('/api/register', methods=['POST'])
def register():
    
    data = request.get_json() or {}
    
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

  

    
    if "@" not in email or "." not in email:
        return jsonify({"error": "Некорректный email"}), 400

    
    if len(password) < 8:
        return jsonify({"error": "Пароль минимум 8 символов"}), 400

    )
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return jsonify({"error": "Email уже зарегистрирован"}), 400
      
    try:
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role="user" 
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"user_id": new_user.id, "message": "Пользователь успешно зарегистрирован"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка при сохранении в базу данных"}), 500
