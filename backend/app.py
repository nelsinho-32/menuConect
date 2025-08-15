from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from decimal import Decimal, InvalidOperation
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps
import json # Essencial para lidar com a lista de preferências

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

# --- Decorator de Autenticação (Protege rotas) ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token em falta!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token é inválido!'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    role, phone, city, uf = data.get('role', 'cliente'), data.get('phone'), data.get('city'), data.get('uf')

    if not all([name, email, password]):
        return jsonify({"error": "Nome, email e senha são obrigatórios."}), 400

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
        if err.errno == 1062:
            return jsonify({"error": "Este email já está a ser utilizado."}), 409
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
            
            # CORREÇÃO: Converte a string de preferências do DB para uma lista
            preferences = json.loads(user['preferences']) if user.get('preferences') else []
            
            return jsonify({
                "token": token,
                "user": { "id": user['id'], "name": user['name'], "email": user['email'], "role": user['role'], "phone": user.get('phone'), "city": user.get('city'), "uf": user.get('uf'), "avatarUrl": user.get('avatarUrl'), "preferences": preferences }
            })
        else:
            return jsonify({"error": "Credenciais inválidas."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROTA DE PERFIL ---

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user_id):
    data = request.get_json()
    
    # CORREÇÃO: Converte a lista de preferências recebida do frontend para uma string JSON
    preferences_json = json.dumps(data.get('preferences', []))

    sql = "UPDATE users SET name = %s, email = %s, phone = %s, city = %s, uf = %s, avatarUrl = %s, preferences = %s WHERE id = %s"
    val = (data.get('name'), data.get('email'), data.get('phone'), data.get('city'), data.get('uf'), data.get('avatarUrl'), preferences_json, current_user_id)

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        # Retorna o objeto de usuário completo, com as preferências como uma lista
        return jsonify({"message": "Perfil atualizado com sucesso!", "user": {**data, 'id': current_user_id}})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# --- ROTAS DE RESTAURANTES ---

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM restaurants")
        restaurants = cursor.fetchall()
        for restaurant in restaurants:
            restaurant['location'] = {'lat': restaurant.pop('lat'), 'lng': restaurant.pop('lng')}
            cursor.execute("SELECT id, name AS dishName, description, price, imageUrl, category, restaurant_id FROM dishes WHERE restaurant_id = %s", (restaurant['id'],)) 
            restaurant['menu'] = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(restaurants)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/api/restaurants', methods=['POST'])
@token_required
def add_restaurant(current_user_id):
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
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# --- ROTA DE PRATOS ---

@app.route('/api/dishes', methods=['POST'])
@token_required
def add_dish(current_user_id):
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM restaurants WHERE name = %s", (data['restaurantName'],))
        restaurant = cursor.fetchone()
        if not restaurant:
            return jsonify({"error": "Restaurante não encontrado."}), 404
        
        sql = "INSERT INTO dishes (name, description, price, imageUrl, category, restaurant_id) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data.get('dishName'), data.get('description'), Decimal(data.get('price')), data.get('imageUrl'), data.get('category'), restaurant['id'])
        cursor.execute(sql, val)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Prato adicionado!", "id": new_id}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
# --- ROTAS DE RESTAURANTES FAVORITOS ---

@app.route('/api/favorites/restaurants', methods=['GET'])
@token_required
def get_favorite_restaurants(current_user_id):
    """Busca os IDs de todos os restaurantes favoritados pelo usuário logado."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT restaurant_id FROM favorite_restaurants WHERE user_id = %s", (current_user_id,))
        # Extrai os IDs da tupla para uma lista simples, ex: [1, 5, 12]
        favorite_ids = [item[0] for item in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(favorite_ids)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/restaurants', methods=['POST'])
@token_required
def add_favorite_restaurant(current_user_id):
    """Adiciona um restaurante à lista de favoritos do usuário."""
    data = request.get_json()
    restaurant_id = data.get('restaurantId')
    if not restaurant_id:
        return jsonify({"error": "restaurantId em falta"}), 400

    sql = "INSERT INTO favorite_restaurants (user_id, restaurant_id) VALUES (%s, %s)"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user_id, restaurant_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Restaurante favoritado com sucesso!"}), 201
    except mysql.connector.Error as err:
        # Ignora o erro se o favorito já existir
        if err.errno == 1062: # Duplicate entry
            return jsonify({"message": "Restaurante já estava nos favoritos."}), 200
        return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/restaurants/<int:restaurant_id>', methods=['DELETE'])
@token_required
def remove_favorite_restaurant(current_user_id, restaurant_id):
    """Remove um restaurante da lista de favoritos do usuário."""
    sql = "DELETE FROM favorite_restaurants WHERE user_id = %s AND restaurant_id = %s"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user_id, restaurant_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Restaurante removido dos favoritos."})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# --- ROTAS DE PRATOS FAVORITOS ---

@app.route('/api/favorites/dishes', methods=['GET'])
@token_required
def get_favorite_dishes(current_user_id):
    """Busca os IDs de todos os pratos favoritados pelo usuário logado."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT dish_id FROM favorite_dishes WHERE user_id = %s", (current_user_id,))
        favorite_ids = [item[0] for item in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(favorite_ids)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/dishes', methods=['POST'])
@token_required
def add_favorite_dish(current_user_id):
    """Adiciona um prato à lista de favoritos do usuário."""
    data = request.get_json()
    dish_id = data.get('dishId')
    if not dish_id:
        return jsonify({"error": "dishId em falta"}), 400

    sql = "INSERT INTO favorite_dishes (user_id, dish_id) VALUES (%s, %s)"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user_id, dish_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Prato favoritado com sucesso!"}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062: # Duplicate entry
            return jsonify({"message": "Prato já estava nos favoritos."}), 200
        return jsonify({"error": str(err)}), 500

@app.route('/api/favorites/dishes/<int:dish_id>', methods=['DELETE'])
@token_required
def remove_favorite_dish(current_user_id, dish_id):
    """Remove um prato da lista de favoritos do usuário."""
    sql = "DELETE FROM favorite_dishes WHERE user_id = %s AND dish_id = %s"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user_id, dish_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Prato removido dos favoritos."})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# --- Executar a Aplicação ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)