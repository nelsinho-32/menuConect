# backend/app.py (VERSÃO COMPLETA E SEM DUPLICADOS)

from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from decimal import Decimal
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps
import json

# --- Configuração ---
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'esta-e-uma-chave-muito-secreta'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Deusefiel1.', # <-- Lembre-se de colocar a sua senha
    'database': 'menu_connect'
}

# --- Decorator de Autenticação ---
def token_required(roles=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
            if not token: return jsonify({'message': 'Token em falta!'}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE id = %s", (data['user_id'],))
                current_user = cursor.fetchone()
                cursor.close()
                conn.close()
                if not current_user: return jsonify({'message': 'Usuário do token não encontrado.'}), 401
                if roles and current_user['role'] not in roles: return jsonify({'message': 'Permissão negada!'}), 403
            except: return jsonify({'message': 'Token é inválido!'}), 401
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

# --- ROTAS DE AUTENTICAÇÃO ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    role, phone, city, uf = data.get('role', 'cliente'), data.get('phone'), data.get('city'), data.get('uf')
    if not all([name, email, password]): return jsonify({"error": "Nome, email e senha são obrigatórios."}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    sql = "INSERT INTO users (name, email, password_hash, role, phone, city, uf) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (name, email, hashed_password, role, phone, city, uf)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Usuário registado com sucesso!"}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062: return jsonify({"error": "Este email já está a ser utilizado."}), 409
        return jsonify({"error": str(err)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    if not email or not password: return jsonify({"error": "Email e senha são obrigatórios."}), 400
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            token = jwt.encode({'user_id': user['id'], 'role': user['role'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
            preferences = json.loads(user['preferences']) if user.get('preferences') else []
            return jsonify({
                "token": token,
                "user": { "id": user['id'], "name": user['name'], "email": user['email'], "role": user['role'], "phone": user.get('phone'), "city": user.get('city'), "uf": user.get('uf'), "avatarUrl": user.get('avatarUrl'), "preferences": preferences, "restaurant_id": user.get('restaurant_id') }
            })
        else: return jsonify({"error": "Credenciais inválidas."}), 401
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- ROTA DE PERFIL ---
@app.route('/api/profile', methods=['PUT'])
@token_required()
def update_profile(current_user):
    data = request.get_json()
    preferences_json = json.dumps(data.get('preferences', []))
    sql = "UPDATE users SET name = %s, email = %s, phone = %s, city = %s, uf = %s, avatarUrl = %s, preferences = %s WHERE id = %s"
    val = (data.get('name'), data.get('email'), data.get('phone'), data.get('city'), data.get('uf'), data.get('avatarUrl'), preferences_json, current_user['id'])
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Perfil atualizado com sucesso!", "user": {**data, 'id': current_user['id']}})
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

# --- ROTAS DE RESTAURANTES ---
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM restaurants")
        restaurants = cursor.fetchall()
        for r in restaurants:
            r['location'] = {'lat': r.pop('lat'), 'lng': r.pop('lng')}
            cursor.execute("SELECT id, name AS dishName, description, price, imageUrl, category, restaurant_id FROM dishes WHERE restaurant_id = %s", (r['id'],))
            r['menu'] = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(restaurants)
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

@app.route('/api/restaurants', methods=['POST'])
@token_required(roles=['admin'])
def add_restaurant(current_user):
    data = request.get_json()
    location = data.get('location', {})
    val = (data.get('name'), data.get('cuisine'), data.get('city'), location.get('lat'), location.get('lng'), data.get('imageUrl'), data.get('logoUrl'), data.get('isNew', True))
    sql = "INSERT INTO restaurants (name, cuisine, city, lat, lng, imageUrl, logoUrl, isNew) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Restaurante adicionado!", "id": new_id}), 201
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

# --- ROTA DE PRATOS ---
@app.route('/api/dishes', methods=['POST'])
@token_required(roles=['admin', 'empresa'])
def add_dish(current_user):
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM restaurants WHERE name = %s", (data['restaurantName'],))
        restaurant = cursor.fetchone()
        if not restaurant: return jsonify({"error": "Restaurante não encontrado."}), 404
        if current_user['role'] == 'empresa' and restaurant['id'] != current_user.get('restaurant_id'):
            return jsonify({"error": "Permissão negada para este restaurante."}), 403
        
        sql = "INSERT INTO dishes (name, description, price, imageUrl, category, restaurant_id) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data.get('dishName'), data.get('description'), Decimal(data.get('price')), data.get('imageUrl'), data.get('category'), restaurant['id'])
        cursor.execute(sql, val)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Prato adicionado!", "id": new_id}), 201
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

# --- ROTAS DE FAVORITOS ---
@app.route('/api/favorites/restaurants', methods=['GET'])
@token_required()
def get_favorite_restaurants(current_user):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT restaurant_id FROM favorite_restaurants WHERE user_id = %s", (current_user['id'],))
        favorite_ids = [item[0] for item in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(favorite_ids)
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/restaurants', methods=['POST'])
@token_required()
def add_favorite_restaurant(current_user):
    data = request.get_json()
    restaurant_id = data.get('restaurantId')
    if not restaurant_id: return jsonify({"error": "restaurantId em falta"}), 400
    sql = "INSERT INTO favorite_restaurants (user_id, restaurant_id) VALUES (%s, %s)"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user['id'], restaurant_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Restaurante favoritado!"}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062: return jsonify({"message": "Já estava nos favoritos."}), 200
        return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/restaurants/<int:restaurant_id>', methods=['DELETE'])
@token_required()
def remove_favorite_restaurant(current_user, restaurant_id):
    sql = "DELETE FROM favorite_restaurants WHERE user_id = %s AND restaurant_id = %s"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user['id'], restaurant_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Restaurante removido dos favoritos."})
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/dishes', methods=['GET'])
@token_required()
def get_favorite_dishes(current_user):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT dish_id FROM favorite_dishes WHERE user_id = %s", (current_user['id'],))
        favorite_ids = [item[0] for item in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(favorite_ids)
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/dishes', methods=['POST'])
@token_required()
def add_favorite_dish(current_user):
    data = request.get_json()
    dish_id = data.get('dishId')
    if not dish_id: return jsonify({"error": "dishId em falta"}), 400
    sql = "INSERT INTO favorite_dishes (user_id, dish_id) VALUES (%s, %s)"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user['id'], dish_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Prato favoritado!"}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062: return jsonify({"message": "Já estava nos favoritos."}), 200
        return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/dishes/<int:dish_id>', methods=['DELETE'])
@token_required()
def remove_favorite_dish(current_user, dish_id):
    sql = "DELETE FROM favorite_dishes WHERE user_id = %s AND dish_id = %s"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user['id'], dish_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Prato removido dos favoritos."})
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500

# --- Executar a Aplicação ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)