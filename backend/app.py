print("--- O SERVIDOR FOI REINICIADO COM O CÓDIGO CORRETO! ---")

from flask import Flask, jsonify, request, url_for
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
        cursor.execute("SELECT id, name, cuisine, city, lat, lng, imageUrl, logoUrl, isNew, map_layout FROM restaurants")
        restaurants = cursor.fetchall()

        for r in restaurants:
            r['location'] = {'lat': r.pop('lat'), 'lng': r.pop('lng')}
            
            # CORREÇÃO PARA CARREGAR O MAPA:
            # Se a coluna map_layout tiver dados, o Python carrega-os como string.
            # json.loads() transforma essa string de volta num objeto/dicionário.
            map_layout_data = json.loads(r['map_layout']) if r.get('map_layout') else {}
            r['tables'] = map_layout_data.get('tables', [])
            r['mapElements'] = map_layout_data.get('mapElements', [])
            r['floorPatternId'] = map_layout_data.get('floorPatternId', 'floor-marble')
            r.pop('map_layout', None) # Remove a coluna original para não ser enviada.

            cursor.execute("SELECT id, name AS dishName, description, price, imageUrl, category, restaurant_id FROM dishes WHERE restaurant_id = %s", (r['id'],))
            r['menu'] = cursor.fetchall()
            
        cursor.close()
        conn.close()
        return jsonify(restaurants)
    except mysql.connector.Error as err: 
        return jsonify({"error": str(err)}), 500

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
    
# --- ROTAS DE RESERVAS ---
@app.route('/api/reservations', methods=['POST'])
@token_required()
def create_reservation(current_user):
    data = request.get_json()
    
    # --- A CORREÇÃO ESTÁ AQUI ---
    # A variável 'booking_time_str' estava em falta na extração de dados.
    restaurant_id = data.get('restaurantId')
    table_id = data.get('tableId')
    booking_time_str = data.get('bookingTime')
    guests = data.get('guests')
    # ---------------------------

    if not all([restaurant_id, table_id, booking_time_str, guests]):
        return jsonify({"error": "Todos os campos da reserva são obrigatórios."}), 400
    
    booking_time_mysql = booking_time_str
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        check_sql = "SELECT id FROM reservations WHERE restaurant_id = %s AND table_id = %s AND booking_time = %s AND status IN ('confirmed', 'pending')"
        cursor.execute(check_sql, (restaurant_id, table_id, booking_time_mysql))
        if cursor.fetchone():
            return jsonify({"error": "Esta mesa já está reservada para este horário."}), 409

        sql = "INSERT INTO reservations (user_id, restaurant_id, table_id, booking_time, guests, status) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (current_user['id'], restaurant_id, table_id, booking_time_mysql, guests, 'pending')
        cursor.execute(sql, val)
        conn.commit()
        new_id = cursor.lastrowid
        
        # ATUALIZA O STATUS DA MESA NO MAPA PARA 'occupied'
        cursor.execute("SELECT map_layout FROM restaurants WHERE id = %s", (restaurant_id,))
        result = cursor.fetchone()
        if result and result['map_layout']:
            map_layout = json.loads(result['map_layout'])
            for table in map_layout.get('tables', []):
                if str(table.get('id')) == str(table_id):
                    table['status'] = 'occupied'
                    break
            updated_map_json = json.dumps(map_layout)
            cursor.execute("UPDATE restaurants SET map_layout = %s WHERE id = %s", (updated_map_json, restaurant_id))
            conn.commit()
        
        return jsonify({"message": "Reserva criada com sucesso!", "reservationId": new_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            

@app.route('/api/my-reservations', methods=['GET'])
@token_required()
def get_my_reservations(current_user):
    """Busca todas as reservas ativas para o usuário logado."""
    sql = """
        SELECT 
            r.id, 
            r.restaurant_id AS restaurantId,
            res.name AS restaurantName,
            res.imageUrl AS restaurantImage,
            r.table_id AS tableId,
            r.booking_time AS bookingTime,
            r.guests,
            r.status
        FROM reservations r
        JOIN restaurants res ON r.restaurant_id = res.id
        WHERE r.user_id = %s AND r.status IN ('confirmed', 'pending')
        ORDER BY r.booking_time ASC
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (current_user['id'],))
        reservations = cursor.fetchall()
        
        # Converte o objeto datetime para uma string no formato ISO para ser compatível com JSON
        for res in reservations:
            if isinstance(res['bookingTime'], datetime.datetime):
                res['bookingTime'] = res['bookingTime'].isoformat()

        cursor.close()
        conn.close()
        return jsonify(reservations)
    except mysql.connector.Error as err:
        print(f"Erro do MySQL ao buscar reservas: {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/api/restaurants/<int:restaurant_id>/map', methods=['PUT'])
@token_required(roles=['admin', 'empresa'])
def update_restaurant_map(current_user, restaurant_id):
    if current_user['role'] == 'empresa' and current_user.get('restaurant_id') != restaurant_id:
        return jsonify({"error": "Permissão negada para editar este mapa."}), 403
    data = request.get_json()
    map_layout_json = json.dumps(data)
    sql = "UPDATE restaurants SET map_layout = %s WHERE id = %s"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (map_layout_json, restaurant_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Mapa atualizado com sucesso!"})
    except mysql.connector.Error as err: return jsonify({"error": str(err)}), 500
    
# --- ROTA PARA CANCELAR RESERVA ---
@app.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
@token_required()
def cancel_reservation(current_user, reservation_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Primeiro, busca os detalhes da reserva para saber qual mesa e restaurante
        cursor.execute("SELECT restaurant_id, table_id FROM reservations WHERE id = %s AND user_id = %s", (reservation_id, current_user['id']))
        reservation_to_cancel = cursor.fetchone()

        if not reservation_to_cancel:
            return jsonify({"error": "Reserva não encontrada ou permissão negada."}), 404
        
        restaurant_id = reservation_to_cancel['restaurant_id']
        table_id = reservation_to_cancel['table_id']

        # 2. Apaga a reserva
        cursor.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))

        # 3. ATUALIZA O STATUS DA MESA NO MAPA PARA 'available'
        cursor.execute("SELECT map_layout FROM restaurants WHERE id = %s", (restaurant_id,))
        result = cursor.fetchone()
        if result and result['map_layout']:
            map_layout = json.loads(result['map_layout'])
            for table in map_layout.get('tables', []):
                if str(table.get('id')) == str(table_id):
                    table['status'] = 'available'
                    break
            
            updated_map_json = json.dumps(map_layout)
            cursor.execute("UPDATE restaurants SET map_layout = %s WHERE id = %s", (updated_map_json, restaurant_id))
            
        conn.commit()
        return jsonify({"message": "Reserva cancelada com sucesso."})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --- ROTAS PARA FILA DE ESPERA (WAITLIST) ---
@app.route('/api/waitlist', methods=['POST'])
@token_required()
def join_waitlist(current_user):
    """Adiciona o usuário à fila de espera de um restaurante."""
    data = request.get_json()
    restaurant_id = data.get('restaurantId')
    if not restaurant_id:
        return jsonify({"error": "restaurantId em falta."}), 400

    sql = "INSERT INTO waitlist (user_id, restaurant_id) VALUES (%s, %s)"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user['id'], restaurant_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Você entrou na fila de espera!"}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062: # Entrada duplicada
            return jsonify({"message": "Você já está nesta fila de espera."}), 200
        return jsonify({"error": str(err)}), 500

@app.route('/api/my-waitlist', methods=['GET'])
@token_required()
def get_my_waitlist(current_user):
    """Busca as filas de espera ativas do usuário."""
    sql = """
        SELECT 
            w.id,
            w.restaurant_id AS restaurantId,
            res.name AS restaurantName,
            res.imageUrl AS restaurantImage,
            (SELECT COUNT(*) + 1 FROM waitlist w2 WHERE w2.restaurant_id = w.restaurant_id AND w2.id < w.id) AS position
        FROM waitlist w
        JOIN restaurants res ON w.restaurant_id = res.id
        WHERE w.user_id = %s
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (current_user['id'],))
        waitlist_entries = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(waitlist_entries)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@app.route('/api/waitlist/<int:restaurant_id>', methods=['DELETE'])
@token_required()
def leave_waitlist(current_user, restaurant_id):
    """Remove o usuário da fila de espera de um restaurante."""
    sql = "DELETE FROM waitlist WHERE user_id = %s AND restaurant_id = %s"
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (current_user['id'], restaurant_id))
        conn.commit()
        
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        
        if success:
            return jsonify({"message": "Você saiu da fila de espera."})
        else:
            return jsonify({"error": "Entrada na fila de espera não encontrada."}), 404
            
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
# ROTA UNIFICADA PARA ATUALIZAR STATUS (CONFIRMAR/CANCELAR)
@app.route('/api/reservations/<int:reservation_id>/status', methods=['PUT'])
@token_required()
def update_reservation_status(current_user, reservation_id):
    data = request.get_json()
    new_status = data.get('status') # Espera receber 'confirmed' ou 'cancelled'

    if new_status not in ['confirmed', 'cancelled']:
        return jsonify({"error": "Status inválido."}), 400

    sql = "UPDATE reservations SET status = %s WHERE id = %s AND user_id = %s"
    val = (new_status, reservation_id, current_user['id'])

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": f"Reserva atualizada para {new_status}."})
        else:
            return jsonify({"error": "Reserva não encontrada ou permissão negada."}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
# ROTA ÚNICA PARA ATUALIZAR (CONFIRMAR) E DELETAR (CANCELAR)
@app.route('/api/reservations/<int:reservation_id>', methods=['PUT', 'DELETE'])
@token_required()
def manage_reservation(current_user, reservation_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        if request.method == 'PUT':
            # Lógica de confirmação
            sql = "UPDATE reservations SET status = 'confirmed' WHERE id = %s AND user_id = %s"
            success_message = "Reserva confirmada com sucesso."
        elif request.method == 'DELETE':
            # Lógica de cancelamento
            sql = "DELETE FROM reservations WHERE id = %s AND user_id = %s"
            success_message = "Reserva cancelada com sucesso."

        cursor.execute(sql, (reservation_id, current_user['id']))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": success_message})
        else:
            return jsonify({"error": "Reserva não encontrada ou permissão negada."}), 404
            
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    
# --- ROTA DE DEPURAÇÃO ---
@app.route('/debug-routes')
def list_routes():
    """Lista todas as rotas registadas na aplicação de forma segura."""
    output = []
    for rule in app.url_map.iter_rules():
        # Exclui a rota 'static' padrão e a própria rota de debug
        if rule.endpoint not in ('static', 'list_routes'):
            methods = ','.join(sorted([m for m in rule.methods if m not in ['HEAD', 'OPTIONS']]))
            line = {"rule": rule.rule, "endpoint": rule.endpoint, "methods": methods}
            output.append(line)
            
    return jsonify(sorted(output, key=lambda r: r['rule']))

# --- Executar a Aplicação ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)