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
        
        # --- INÍCIO DA CORREÇÃO: Adiciona average_rating e review_count à query ---
        cursor.execute("SELECT id, name, cuisine, city, lat, lng, imageUrl, logoUrl, isNew, map_layout, galleryUrls, average_rating, review_count FROM restaurants")
        # --- FIM DA CORREÇÃO ---
        
        restaurants = cursor.fetchall()

        for r in restaurants:
            r['location'] = {'lat': r.pop('lat'), 'lng': r.pop('lng')}
            
            try:
                map_layout_data = json.loads(r['map_layout']) if r.get('map_layout') else {}
            except (json.JSONDecodeError, TypeError):
                map_layout_data = {}
            r['tables'] = map_layout_data.get('tables', [])
            r['mapElements'] = map_layout_data.get('mapElements', [])
            r['floorPatternId'] = map_layout_data.get('floorPatternId', 'floor-marble')
            r.pop('map_layout', None)

            try:
                gallery_urls_str = r.get('galleryUrls')
                r['galleryUrls'] = json.loads(gallery_urls_str) if isinstance(gallery_urls_str, str) else []
            except (json.JSONDecodeError, TypeError):
                r['galleryUrls'] = []
                
            if r.get('average_rating') is not None:
                r['average_rating'] = float(r['average_rating'])
            
            cursor.execute("SELECT id, name AS dishName, description, price, imageUrl, category, restaurant_id FROM dishes WHERE restaurant_id = %s", (r['id'],))
            r['menu'] = cursor.fetchall()
            
            promo_sql = "SELECT id, title, description, discount_type, discount_value FROM promotions WHERE restaurant_id = %s AND active = TRUE AND (end_date IS NULL OR end_date >= CURDATE())"
            cursor.execute(promo_sql, (r['id'],))
            promotions = cursor.fetchall()
            for promo in promotions:
                if isinstance(promo['discount_value'], Decimal):
                    promo['discount_value'] = float(promo['discount_value'])
            r['promotions'] = promotions
            
            for dish in r['menu']:
                dish['restaurantName'] = r['name']
                dish['restaurantId'] = r['id']
            
        cursor.close()
        conn.close()
        return jsonify(restaurants)
        
    except mysql.connector.Error as err: 
        print(f"ERRO DE BANCO DE DADOS em get_restaurants: {err}") 
        return jsonify({"error": f"Erro de banco de dados: {err}"}), 500
    except Exception as e:
        print(f"ERRO INESPERADO em get_restaurants: {e}")
        return jsonify({"error": f"Erro inesperado no servidor: {e}"}), 500

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
    
@app.route('/api/dishes/<int:dish_id>', methods=['DELETE'])
@token_required(roles=['admin', 'empresa'])
def delete_dish(current_user, dish_id):
    """Exclui um prato, com verificação de permissão."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Busca o prato para verificar a quem pertence.
        cursor.execute("SELECT restaurant_id FROM dishes WHERE id = %s", (dish_id,))
        dish = cursor.fetchone()

        if not dish:
            cursor.close()
            conn.close()
            return jsonify({"error": "Prato não encontrado."}), 404

        # 2. Lógica de Autorização
        # Se o usuário for 'empresa', verifica se o prato pertence ao seu restaurante.
        if current_user['role'] == 'empresa':
            if dish['restaurant_id'] != current_user.get('restaurant_id'):
                cursor.close()
                conn.close()
                return jsonify({"error": "Permissão negada para excluir este prato."}), 403
        
        # Se for 'admin', a verificação acima é ignorada e ele pode prosseguir.

        # 3. Exclui o prato
        cursor.execute("DELETE FROM dishes WHERE id = %s", (dish_id,))
        conn.commit()

        cursor.close()
        conn.close()
        
        return jsonify({"message": "Prato excluído com sucesso!"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

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
    restaurant_id = data.get('restaurantId')
    table_id = data.get('tableId')
    booking_time_str = data.get('bookingTime')
    guests = data.get('guests')
    encontro_id = data.get('encontroId') # Recebe o ID do encontro (pode ser Nulo)
    status = data.get('status', 'pending') # Recebe o status ('confirmed' ou 'pending')

    if not all([restaurant_id, table_id, booking_time_str, guests]):
        return jsonify({"error": "Todos os campos da reserva são obrigatórios."}), 400

    booking_time_mysql = booking_time_str
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Verifica se a reserva já existe
        check_sql = "SELECT id FROM reservations WHERE restaurant_id = %s AND table_id = %s AND booking_time = %s AND status IN ('confirmed', 'pending')"
        cursor.execute(check_sql, (restaurant_id, table_id, booking_time_mysql))
        if cursor.fetchone():
            return jsonify({"error": "Esta mesa já está reservada para este horário."}), 409

        # --- A CORREÇÃO ESTÁ AQUI ---
        # A query SQL agora inclui a coluna 'encontro_id'
        sql = """
            INSERT INTO reservations 
            (user_id, restaurant_id, table_id, booking_time, guests, status, encontro_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        # A lista de valores agora inclui a variável 'encontro_id'
        val = (current_user['id'], restaurant_id, table_id, booking_time_mysql, guests, status, encontro_id)
        # --- FIM DA CORREÇÃO ---
        
        cursor.execute(sql, val)
        new_id = cursor.lastrowid

        # Atualiza o status da mesa no mapa para 'occupied'
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
    """
    Busca todas as reservas ativas para o usuário logado,
    depois de limpar automaticamente as que já expiraram.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # --- A CORREÇÃO ESTÁ AQUI ---
        # 1. Primeiro, atualiza o status de todas as reservas passadas do usuário para 'completed'.
        # NOW() pega na data e hora atuais do servidor do banco de dados.
        cleanup_sql = """
            UPDATE reservations 
            SET status = 'completed' 
            WHERE user_id = %s 
            AND booking_time < NOW() 
            AND status IN ('confirmed', 'pending')
        """
        cursor.execute(cleanup_sql, (current_user['id'],))
        conn.commit()
        # --- FIM DA CORREÇÃO ---

        # 2. Agora, busca as reservas que AINDA estão ativas.
        # A query SELECT não precisa de ser alterada, pois ela já filtra por 'confirmed' e 'pending'.
        # As reservas que acabámos de marcar como 'completed' serão naturalmente ignoradas.
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
        cursor.execute(sql, (current_user['id'],))
        reservations = cursor.fetchall()
        
        # Formata a data para ser facilmente lida pelo JavaScript
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

# --- ROTAS DE GESTÃO PARA EMPRESAS E ADMINS ---

@app.route('/api/management/reservations', methods=['GET'])
@token_required(roles=['admin', 'empresa'])
def get_management_reservations(current_user):
    """Busca todas as reservas ativas para o restaurante, incluindo detalhes do encontro se houver."""
    
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = request.args.get('restaurant_id')
        if not restaurant_id:
            return jsonify({"error": "Admin deve especificar um restaurant_id"}), 400

    if not restaurant_id:
        return jsonify({"error": "Usuário empresa não está associado a um restaurante."}), 403

    # --- INÍCIO DA CORREÇÃO ---
    # A query SQL foi expandida para buscar dados da tabela 'encontros'
    sql = """
        SELECT 
            r.id, r.table_id, r.booking_time, r.guests, r.status, 
            u.name as user_name, u.phone as user_phone,
            e.id as encontro_id, e.payment_option
        FROM reservations r
        JOIN users u ON r.user_id = u.id
        LEFT JOIN encontros e ON r.encontro_id = e.id
        WHERE r.restaurant_id = %s AND r.status IN ('confirmed', 'pending')
        ORDER BY r.booking_time ASC
    """
    # --- FIM DA CORREÇÃO ---
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (restaurant_id,))
        reservations = cursor.fetchall()
        
        # Para cada reserva que veio de um encontro, busca os detalhes dos convidados
        for res in reservations:
            if res.get('encontro_id'):
                guest_sql = "SELECT guest_name, menu_selection FROM encontro_guests WHERE encontro_id = %s"
                cursor.execute(guest_sql, (res['encontro_id'],))
                guests_details = cursor.fetchall()
                
                # Processa o JSON do menu para ser mais legível
                for guest in guests_details:
                    guest['menu_selection'] = json.loads(guest['menu_selection'])
                res['encontro_details'] = guests_details
            
            if isinstance(res['booking_time'], datetime.datetime):
                res['booking_time'] = res['booking_time'].isoformat()
                
        cursor.close()
        conn.close()
        return jsonify(reservations)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route('/api/management/waitlist', methods=['GET'])
@token_required(roles=['admin', 'empresa'])
def get_management_waitlist(current_user):
    """Busca a fila de espera para o restaurante do usuário logado."""
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin' and not restaurant_id:
        restaurant_id = request.args.get('restaurant_id')
        if not restaurant_id:
            return jsonify({"error": "Admin deve especificar um restaurant_id"}), 400
    
    if not restaurant_id:
        return jsonify({"error": "Usuário empresa não está associado a um restaurante."}), 403

    sql = """
        SELECT u.name as user_name, u.phone, w.created_at
        FROM waitlist w
        JOIN users u ON w.user_id = u.id
        WHERE w.restaurant_id = %s
        ORDER BY w.created_at ASC
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (restaurant_id,))
        waitlist = cursor.fetchall()
        for entry in waitlist:
            if isinstance(entry['created_at'], datetime.datetime):
                entry['created_at'] = entry['created_at'].isoformat()
        cursor.close()
        conn.close()
        return jsonify(waitlist)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route('/api/management/tables/<string:table_id>/status', methods=['PUT'])
@token_required(roles=['admin', 'empresa'])
def update_table_status_management(current_user, table_id):
    """Atualiza o status de uma mesa específica."""
    data = request.get_json()
    new_status = data.get('status')
    # O ID do restaurante agora vem no corpo do pedido.
    restaurant_id = data.get('restaurantId')
    
    if not restaurant_id:
        return jsonify({"error": "restaurantId é obrigatório."}), 400

    # Lógica de permissão
    if current_user['role'] == 'empresa' and current_user.get('restaurant_id') != restaurant_id:
        return jsonify({"error": "Permissão negada para editar este mapa."}), 403
    
    if new_status not in ['available', 'occupied', 'cleaning']:
        return jsonify({"error": "Status inválido."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Pega o mapa atual
        cursor.execute("SELECT map_layout FROM restaurants WHERE id = %s", (restaurant_id,))
        result = cursor.fetchone()
        if not (result and result['map_layout']):
            return jsonify({"error": "Layout do mapa não encontrado."}), 404

        map_layout = json.loads(result['map_layout'])
        table_found = False
        for table in map_layout.get('tables', []):
            if str(table.get('id')) == str(table_id):
                table['status'] = new_status
                table_found = True
                break
        
        if not table_found:
            return jsonify({"error": f"Mesa '{table_id}' não encontrada no layout."}), 404

        # Salva o mapa atualizado
        updated_map_json = json.dumps(map_layout)
        cursor.execute("UPDATE restaurants SET map_layout = %s WHERE id = %s", (updated_map_json, restaurant_id))
        conn.commit()
        
        return jsonify({"message": f"Status da mesa {table_id} atualizado para {new_status}."})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
# --- ROTAS DE PEDIDOS E FINANCEIRO ---

@app.route('/api/orders', methods=['POST'])
@token_required()
def create_order(current_user):
    """Cria um novo pedido a partir dos dados do carrinho."""
    data = request.get_json()
    cart_items = data.get('cartItems')
    total_price = data.get('totalPrice')
    reservation_id = data.get('reservationId')
    
    if not cart_items or not total_price:
        return jsonify({"error": "Dados do pedido incompletos."}), 400

    # Agrupa os itens por restaurante para criar um pedido para cada um
    orders_by_restaurant = {}
    for item in cart_items:
        restaurant_id = item.get('restaurantId')
        if restaurant_id not in orders_by_restaurant:
            orders_by_restaurant[restaurant_id] = {'items': [], 'subtotal': 0}
        orders_by_restaurant[restaurant_id]['items'].append(item)
        orders_by_restaurant[restaurant_id]['subtotal'] += Decimal(item.get('price', 0)) * int(item.get('quantity', 0))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        for restaurant_id, order_data in orders_by_restaurant.items():
            # 1. Cria a entrada principal na tabela 'orders'
            order_sql = "INSERT INTO orders (user_id, restaurant_id, total_price, reservation_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(order_sql, (current_user['id'], restaurant_id, order_data['subtotal'], reservation_id))
            order_id = cursor.lastrowid

            # 2. Insere cada item do pedido na tabela 'order_items'
            for item in order_data['items']:
                item_sql = "INSERT INTO order_items (order_id, dish_id, quantity, price_at_time, customization) VALUES (%s, %s, %s, %s, %s)"
                customization_json = json.dumps(item.get('customization')) if item.get('customization') else None
                cursor.execute(item_sql, (order_id, item['id'], item['quantity'], Decimal(item['price']), customization_json))
        
        conn.commit()
        return jsonify({"message": "Pedido criado com sucesso!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/api/management/financials', methods=['GET'])
@token_required(roles=['admin', 'empresa'])
def get_financial_data(current_user):
    """Calcula e retorna dados financeiros para o restaurante do usuário."""
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = request.args.get('restaurant_id', restaurant_id) # Admin pode especificar

    if not restaurant_id:
        return jsonify({"error": "Nenhum restaurante associado."}), 403

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Calcula as vendas do dia (hoje)
        sales_today_sql = """
            SELECT SUM(total_price) as total
            FROM orders
            WHERE restaurant_id = %s AND DATE(created_at) = CURDATE()
        """
        cursor.execute(sales_today_sql, (restaurant_id,))
        sales_today = cursor.fetchone()['total'] or 0

        # 2. Encontra o prato mais popular
        popular_dish_sql = """
            SELECT d.name as dishName, SUM(oi.quantity) as total_sold
            FROM order_items oi
            JOIN dishes d ON oi.dish_id = d.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.restaurant_id = %s
            GROUP BY d.name
            ORDER BY total_sold DESC
            LIMIT 1
        """
        cursor.execute(popular_dish_sql, (restaurant_id,))
        popular_dish = cursor.fetchone()

        return jsonify({
            "dailySales": float(sales_today),
            "mostPopularDish": popular_dish['dishName'] if popular_dish else "Nenhum pedido"
        })

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --- ROTAS PARA O PLANEADOR DE ENCONTROS ---

@app.route('/api/encontros', methods=['POST'])
@token_required()
def create_encontro(current_user):
    """Cria um novo encontro planeado."""
    data = request.get_json()
    
    # Extrai os dados do encontro
    restaurant_id = data.get('restaurantId')
    table_id = data.get('selectedTable', {}).get('id')
    encontro_time_str = data.get('dateTime') # Espera-se uma string ISO
    payment_option = data.get('paymentOption', 'local')
    guests = data.get('guests', [])

    if not all([restaurant_id, table_id, encontro_time_str, guests]):
        return jsonify({"error": "Dados do encontro incompletos."}), 400

    try:
        # Formata a data para o MySQL
        dt_obj = datetime.datetime.fromisoformat(encontro_time_str.replace('Z', ''))
        encontro_time_mysql = dt_obj.strftime('%Y-%m-%d %H:%M:%S')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 1. Insere o encontro principal na tabela 'encontros'
        encontro_sql = "INSERT INTO encontros (organizer_id, restaurant_id, table_id, encontro_time, payment_option) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(encontro_sql, (current_user['id'], restaurant_id, table_id, encontro_time_mysql, payment_option))
        encontro_id = cursor.lastrowid

        # 2. Insere cada convidado e o seu menu na tabela 'encontro_guests'
        for guest in guests:
            guest_sql = "INSERT INTO encontro_guests (encontro_id, user_id, guest_name, menu_selection) VALUES (%s, %s, %s, %s)"
            # O ID do usuário pode não existir se for um convidado genérico
            user_id = guest.get('id') if isinstance(guest.get('id'), int) else None
            menu_json = json.dumps(guest.get('menu', {}))
            cursor.execute(guest_sql, (encontro_id, user_id, guest.get('name'), menu_json))
        
        conn.commit()
        return jsonify({"message": "Encontro planeado com sucesso!", "encontroId": encontro_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# --- ROTA PARA DETALHES DA MESA NO PAINEL DE GESTÃO ---

@app.route('/api/management/tables/<string:table_id>/details', methods=['GET'])
@token_required(roles=['admin', 'empresa'])
def get_table_details(current_user, table_id):
    """Busca detalhes de uma mesa, priorizando uma sessão ativa e, em seguida, uma reserva confirmada."""
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = request.args.get('restaurant_id', restaurant_id)
    if not restaurant_id:
        return jsonify({"error": "Nenhum restaurante associado."}), 403

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Tenta encontrar uma SESSÃO ATIVA primeiro
        session_sql = "SELECT id as session_id, start_time, guests, customer_names FROM table_sessions WHERE restaurant_id = %s AND table_id = %s AND status = 'active' ORDER BY start_time DESC LIMIT 1"
        cursor.execute(session_sql, (restaurant_id, table_id))
        session = cursor.fetchone()

        if session:
            # Se encontrou uma sessão, busca o consumo dela
            orders_sql = "SELECT oi.quantity, d.name as dishName, oi.price_at_time, oi.customization FROM order_items oi JOIN dishes d ON oi.dish_id = d.id JOIN orders o ON oi.order_id = o.id WHERE o.session_id = %s"
            cursor.execute(orders_sql, (session['session_id'],))
            consumption = cursor.fetchall()
            for item in consumption:
                if item.get('customization'):
                    item['customization'] = json.loads(item['customization'])
            
            response_data = {"type": "session", "details": session, "consumption": consumption}
            return jsonify(response_data)

        # --- INÍCIO DA NOVA LÓGICA ---
        # 2. Se NÃO encontrou sessão ativa, procura por uma RESERVA CONFIRMADA
        reservation_sql = """
            SELECT r.id as reservation_id, r.booking_time, r.guests, r.encontro_id, u.name as user_name, u.phone as user_phone
            FROM reservations r
            JOIN users u ON r.user_id = u.id
            WHERE r.restaurant_id = %s AND r.table_id = %s AND r.status = 'confirmed'
            ORDER BY r.booking_time ASC
            LIMIT 1
        """
        cursor.execute(reservation_sql, (restaurant_id, table_id))
        reservation = cursor.fetchone()

        if reservation:
            consumption = []
            if reservation.get('encontro_id'):
                guest_sql = "SELECT guest_name, menu_selection FROM encontro_guests WHERE encontro_id = %s"
                cursor.execute(guest_sql, (reservation['encontro_id'],))
                guests_details = cursor.fetchall()
                # Transforma o menu em algo parecido com o consumo
                for guest in guests_details:
                    menu = json.loads(guest['menu_selection'])
                    for item_type, item_details in menu.items():
                        if item_details and item_details.get('dishName'):
                             consumption.append(f"({guest['guest_name']}) {item_details['dishName']}")
            
            response_data = {"type": "reservation", "details": reservation, "consumption": consumption}
            return jsonify(response_data)
        # --- FIM DA NOVA LÓGICA ---

        return jsonify({"error": "Nenhuma sessão ativa ou reserva encontrada para esta mesa."}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/my-orders', methods=['GET'])
@token_required()
def get_my_orders(current_user):
    """Busca o histórico de pedidos para o usuário logado com detalhes completos."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Busca todos os pedidos, agora fazendo JOIN com a tabela de reservas
        orders_sql = """
            SELECT 
                o.id, 
                o.total_price, 
                o.created_at,
                r.name as restaurantName,
                res.encontro_id -- <-- A CORREÇÃO ESTÁ AQUI: Busca o ID do encontro na tabela de reservas
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            LEFT JOIN reservations res ON o.reservation_id = res.id -- <-- USA LEFT JOIN para não quebrar pedidos sem reserva
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC
        """
        cursor.execute(orders_sql, (current_user['id'],))
        orders = cursor.fetchall()

        # 2. Para cada pedido, busca os seus itens (código existente, sem alterações)
        for order in orders:
            items_sql = """
                SELECT 
                    oi.quantity, 
                    oi.price_at_time, 
                    oi.customization,
                    d.name as dishName,
                    d.imageUrl as dishImage
                FROM order_items oi
                JOIN dishes d ON oi.dish_id = d.id
                WHERE oi.order_id = %s
            """
            cursor.execute(items_sql, (order['id'],))
            order_items = cursor.fetchall()

            for item in order_items:
                if item['customization']:
                    item['customization'] = json.loads(item['customization']) 
            
            order['items'] = order_items
            
            if isinstance(order['created_at'], datetime.datetime):
                order['created_at'] = order['created_at'].isoformat()

        cursor.close()
        conn.close()
        return jsonify(orders)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
# --- ROTAS PARA O 'CAIXA' / GESTÃO DE SESSÃO DE MESA ---

@app.route('/api/management/sessions', methods=['POST'])
@token_required(roles=['admin', 'empresa'])
def start_table_session(current_user):
    """Inicia um novo atendimento (sessão) para uma mesa."""
    data = request.get_json()
    table_id = data.get('tableId')
    guests = data.get('guests')
    customer_names = data.get('customerNames') # Espera uma lista de nomes
    
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = data.get('restaurantId', restaurant_id) # Admin pode especificar

    if not all([restaurant_id, table_id, guests]):
        return jsonify({"error": "Dados insuficientes para iniciar a sessão."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 1. Inicia a sessão na tabela 'table_sessions'
        sql_session = """
            INSERT INTO table_sessions (restaurant_id, table_id, start_time, guests, customer_names)
            VALUES (%s, %s, %s, %s, %s)
        """
        start_time = datetime.datetime.now()
        customer_names_json = json.dumps(customer_names) if customer_names else None
        cursor.execute(sql_session, (restaurant_id, table_id, start_time, guests, customer_names_json))
        new_session_id = cursor.lastrowid

        # 2. Atualiza o status da mesa no mapa para 'occupied'
        cursor.execute("SELECT map_layout FROM restaurants WHERE id = %s", (restaurant_id,))
        result = cursor.fetchone()
        if result and result[0]: # result[0] é map_layout
            map_layout = json.loads(result[0])
            for table in map_layout.get('tables', []):
                if str(table.get('id')) == str(table_id):
                    table['status'] = 'occupied'
                    break
            updated_map_json = json.dumps(map_layout)
            cursor.execute("UPDATE restaurants SET map_layout = %s WHERE id = %s", (updated_map_json, restaurant_id))

        conn.commit()
        return jsonify({"message": "Sessão iniciada com sucesso!", "sessionId": new_session_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/api/management/sessions/table/<string:table_id>', methods=['GET'])
@token_required(roles=['admin', 'empresa'])
def get_active_session_details_for_table(current_user, table_id):
    """Busca os detalhes da sessão ativa para uma mesa específica."""
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = request.args.get('restaurantId', restaurant_id)
    if not restaurant_id:
        return jsonify({"error": "Nenhum restaurante associado."}), 403

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Busca a sessão ativa
        session_sql = "SELECT id, start_time, guests, customer_names FROM table_sessions WHERE restaurant_id = %s AND table_id = %s AND status = 'active' ORDER BY start_time DESC LIMIT 1"
        cursor.execute(session_sql, (restaurant_id, table_id))
        session = cursor.fetchone()

        if not session:
            return jsonify({"error": "Nenhuma sessão ativa encontrada para esta mesa."}), 404

        # 2. Busca os pedidos (consumo) associados a esta sessão, AGORA COM A PERSONALIZAÇÃO
        orders_sql = """
            SELECT 
                oi.quantity, 
                oi.price_at_time, 
                oi.customization, -- <-- ADICIONADO
                d.name as dishName
            FROM order_items oi
            JOIN dishes d ON oi.dish_id = d.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.session_id = %s
        """
        cursor.execute(orders_sql, (session['id'],))
        consumption = cursor.fetchall()
        
        # Processa os dados para o frontend
        if session.get('start_time'): session['start_time'] = session['start_time'].isoformat()
        if session.get('customer_names'): session['customer_names'] = json.loads(session['customer_names'])
        
        # Processa a personalização de cada item
        for item in consumption:
            if item.get('customization'):
                item['customization'] = json.loads(item['customization'])

        return jsonify({
            "session": session,
            "consumption": consumption
        })

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
# Cole esta nova função no seu backend/app.py

@app.route('/api/management/sessions/<int:session_id>/orders', methods=['POST'])
@token_required(roles=['admin', 'empresa'])
def add_order_to_session(current_user, session_id):
    """Adiciona um novo pedido (um ou mais itens) a uma sessão de mesa existente."""
    data = request.get_json()
    cart_items = data.get('items')
    
    if not cart_items:
        return jsonify({"error": "Nenhum item fornecido para o pedido."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT restaurant_id FROM table_sessions WHERE id = %s", (session_id,))
        session = cursor.fetchone()
        if not session:
            return jsonify({"error": "Sessão não encontrada."}), 404
        
        restaurant_id = session['restaurant_id']
        if current_user['role'] == 'empresa' and current_user.get('restaurant_id') != restaurant_id:
            return jsonify({"error": "Permissão negada para esta sessão."}), 403

        total_price = sum(Decimal(item.get('price', 0)) * int(item.get('quantity', 0)) for item in cart_items)
        
        order_sql = "INSERT INTO orders (user_id, restaurant_id, total_price, session_id, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(order_sql, (current_user['id'], restaurant_id, total_price, session_id, 'in_progress'))
        order_id = cursor.lastrowid

        # --- A CORREÇÃO ESTÁ AQUI ---
        for item in cart_items:
            # Converte o objeto de personalização para uma string JSON para guardar no banco
            customization_json = json.dumps(item.get('customization')) if item.get('customization') else None
            
            # A query SQL agora inclui a coluna 'customization'
            item_sql = "INSERT INTO order_items (order_id, dish_id, quantity, price_at_time, customization) VALUES (%s, %s, %s, %s, %s)"
            # A lista de valores agora inclui a variável 'customization_json'
            cursor.execute(item_sql, (order_id, item['id'], item['quantity'], Decimal(item['price']), customization_json))
        # --- FIM DA CORREÇÃO ---
        
        conn.commit()
        return jsonify({"message": "Pedido adicionado à mesa com sucesso!", "orderId": order_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/management/sessions/<int:session_id>/finish', methods=['PUT'])
@token_required(roles=['admin', 'empresa'])
def finish_table_session(current_user, session_id):
    data = request.get_json()
    payment_method = data.get('paymentMethod')
    if not payment_method:
        return jsonify({"error": "A forma de pagamento é obrigatória."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT restaurant_id, table_id FROM table_sessions WHERE id = %s AND status = 'active'", (session_id,))
        session = cursor.fetchone()
        if not session: return jsonify({"error": "Sessão ativa não encontrada."}), 404
        
        restaurant_id = session['restaurant_id']
        table_id = session['table_id']

        if current_user['role'] == 'empresa' and current_user.get('restaurant_id') != restaurant_id:
            return jsonify({"error": "Permissão negada."}), 403

        # --- CORREÇÃO: Marcar pedidos como 'completed' ---
        cursor.execute("UPDATE orders SET status = 'completed' WHERE session_id = %s", (session_id,))

        sql_session = "UPDATE table_sessions SET status = 'paid', end_time = %s, payment_method = %s WHERE id = %s"
        cursor.execute(sql_session, (datetime.datetime.now(), payment_method, session_id))

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
        return jsonify({"message": "Sessão finalizada com sucesso."})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/management/sessions/from-reservation', methods=['POST'])
@token_required(roles=['admin', 'empresa'])
def start_session_from_reservation(current_user):
    """Cria uma nova sessão a partir de uma reserva existente."""
    data = request.get_json()
    reservation_id = data.get('reservationId')
    if not reservation_id:
        return jsonify({"error": "ID da reserva é obrigatório."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Busca os dados da reserva
        cursor.execute("SELECT * FROM reservations WHERE id = %s AND status = 'confirmed'", (reservation_id,))
        reservation = cursor.fetchone()
        if not reservation:
            return jsonify({"error": "Reserva confirmada não encontrada."}), 404

        restaurant_id = reservation['restaurant_id']
        
        # 2. Inicia a nova sessão
        session_sql = "INSERT INTO table_sessions (restaurant_id, table_id, start_time, guests, reservation_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(session_sql, (restaurant_id, reservation['table_id'], datetime.datetime.now(), reservation['guests'], reservation_id))
        session_id = cursor.lastrowid

        # 3. Se a reserva veio de um encontro, copia os itens para um novo pedido
        if reservation.get('encontro_id'):
            cursor.execute("SELECT menu_selection FROM encontro_guests WHERE encontro_id = %s", (reservation['encontro_id'],))
            guests_menu = cursor.fetchall()
            
            all_items = []
            for guest in guests_menu:
                menu = json.loads(guest['menu_selection'])
                for item_type, item_details in menu.items():
                    if item_details and item_details.get('id'):
                        all_items.append({**item_details, 'quantity': 1})
            
            if all_items:
                total_price = sum(Decimal(item.get('price', 0)) * int(item.get('quantity', 0)) for item in all_items)
                order_sql = "INSERT INTO orders (user_id, restaurant_id, total_price, session_id, status, reservation_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(order_sql, (reservation['user_id'], restaurant_id, total_price, session_id, 'in_progress', reservation_id))
                order_id = cursor.lastrowid
                
                for item in all_items:
                    customization_json = json.dumps(item.get('customization')) if item.get('customization') else None
                    item_sql = "INSERT INTO order_items (order_id, dish_id, quantity, price_at_time, customization) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(item_sql, (order_id, item['id'], item['quantity'], Decimal(item['price']), customization_json))
        
        # 4. Atualiza a reserva original para 'completed' para não aparecer mais
        cursor.execute("UPDATE reservations SET status = 'completed' WHERE id = %s", (reservation_id,))

        conn.commit()
        return jsonify({"message": "Atendimento iniciado com sucesso!", "sessionId": session_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/reviews', methods=['POST'])
@token_required(roles=['cliente', 'admin']) # Apenas clientes podem deixar avaliações
def add_review(current_user):
    """Adiciona uma nova avaliação e recalcula a média do restaurante."""
    data = request.get_json()
    restaurant_id = data.get('restaurantId')
    rating = data.get('rating')
    comment = data.get('comment')

    if not all([restaurant_id, rating]):
        return jsonify({"error": "ID do restaurante e avaliação são obrigatórios."}), 400
    if not 1 <= rating <= 5:
        return jsonify({"error": "A avaliação deve ser entre 1 e 5."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insere a nova avaliação
        sql_insert = "INSERT INTO reviews (restaurant_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_insert, (restaurant_id, current_user['id'], rating, comment))
        
        # Recalcula a média e a contagem de avaliações
        sql_update = """
            UPDATE restaurants r
            SET 
                r.average_rating = (SELECT AVG(rating) FROM reviews WHERE restaurant_id = r.id),
                r.review_count = (SELECT COUNT(*) FROM reviews WHERE restaurant_id = r.id)
            WHERE r.id = %s
        """
        cursor.execute(sql_update, (restaurant_id,))
        
        conn.commit()
        return jsonify({"message": "Avaliação adicionada com sucesso!"}), 201

    except mysql.connector.Error as err:
        if err.errno == 1062: # Chave duplicada
            return jsonify({"error": "Você já avaliou este restaurante."}), 409
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/restaurants/<int:restaurant_id>/reviews', methods=['GET'])
def get_reviews_for_restaurant(restaurant_id):
    """Busca todas as avaliações para um restaurante específico."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT 
                rev.rating, 
                rev.comment, 
                rev.created_at,
                usr.name as userName,
                usr.avatarUrl as userAvatarUrl
            FROM reviews rev
            JOIN users usr ON rev.user_id = usr.id
            WHERE rev.restaurant_id = %s
            ORDER BY rev.created_at DESC
        """
        cursor.execute(sql, (restaurant_id,))
        reviews = cursor.fetchall()

        # Formata a data para ser lida facilmente pelo JavaScript
        for review in reviews:
            if isinstance(review['created_at'], datetime.datetime):
                review['created_at'] = review['created_at'].isoformat()

        cursor.close()
        conn.close()
        return jsonify(reviews)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@app.route('/api/management/analytics', methods=['GET'])
@token_required(roles=['admin', 'empresa'])
def get_analytics_data(current_user):
    """
    Busca dados de análise de vendas para um restaurante num determinado período.
    Aceita o parâmetro 'period' na query string (ex: 'last7days', 'last30days', 'monthToDate').
    """
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = request.args.get('restaurant_id', restaurant_id)
    if not restaurant_id:
        return jsonify({"error": "Nenhum restaurante associado."}), 403

    period = request.args.get('period', 'last7days') # Padrão para os últimos 7 dias

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # --- Lógica para o Histórico de Vendas ---
        # Define o intervalo de datas com base no período solicitado
        if period == 'last30days':
            date_filter = "o.created_at >= CURDATE() - INTERVAL 30 DAY"
        elif period == 'monthToDate':
            date_filter = "YEAR(o.created_at) = YEAR(CURDATE()) AND MONTH(o.created_at) = MONTH(CURDATE())"
        else: # Padrão é 'last7days'
            date_filter = "o.created_at >= CURDATE() - INTERVAL 7 DAY"

        sales_history_sql = f"""
            SELECT 
                DATE(o.created_at) as date, 
                SUM(o.total_price) as total_sales
            FROM orders o
            WHERE o.restaurant_id = %s AND {date_filter}
            GROUP BY DATE(o.created_at)
            ORDER BY date ASC
        """
        cursor.execute(sales_history_sql, (restaurant_id,))
        sales_history = cursor.fetchall()
        
        # Formata a data para ser facilmente lida pelo JavaScript
        for sale in sales_history:
            sale['date'] = sale['date'].strftime('%Y-%m-%d')
            sale['total_sales'] = float(sale['total_sales'])

        # --- Lógica para os Pratos Mais Rentáveis ---
        top_dishes_sql = f"""
            SELECT 
                d.name as dishName,
                SUM(oi.quantity) as total_quantity_sold,
                SUM(oi.quantity * oi.price_at_time) as total_revenue
            FROM order_items oi
            JOIN dishes d ON oi.dish_id = d.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.restaurant_id = %s AND {date_filter}
            GROUP BY d.name
            ORDER BY total_revenue DESC
            LIMIT 5
        """
        cursor.execute(top_dishes_sql, (restaurant_id,))
        top_dishes = cursor.fetchall()

        # Converte Decimals para floats
        for dish in top_dishes:
            dish['total_revenue'] = float(dish['total_revenue'])

        cursor.close()
        conn.close()
        
        return jsonify({
            "sales_history": sales_history,
            "top_dishes": top_dishes
        })

    except mysql.connector.Error as err:
        print(f"ERRO DE BANCO DE DADOS em get_analytics_data: {err}")
        return jsonify({"error": str(err)}), 500
    
@app.route('/api/management/promotions', methods=['POST'])
@token_required(roles=['admin', 'empresa'])
def create_promotion(current_user):
    """Cria uma nova promoção para um restaurante."""
    data = request.get_json()
    
    # O ID do restaurante é obrigatório. Para 'empresa', vem do token. Para 'admin', vem do corpo do pedido.
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = data.get('restaurantId', restaurant_id)

    if not restaurant_id:
        return jsonify({"error": "Restaurante não identificado."}), 400

    # Validação dos dados recebidos
    title = data.get('title')
    discount_type = data.get('discount_type')
    discount_value = data.get('discount_value')
    if not all([title, discount_type, discount_value]):
        return jsonify({"error": "Título, tipo de desconto e valor são obrigatórios."}), 400

    sql = """
        INSERT INTO promotions (restaurant_id, title, description, discount_type, discount_value, start_date, end_date, active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (
        restaurant_id,
        title,
        data.get('description'),
        discount_type,
        Decimal(discount_value),
        data.get('start_date') or None, # Permite datas nulas
        data.get('end_date') or None,
        data.get('active', True)
    )

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Promoção criada com sucesso!", "promotionId": new_id}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route('/api/management/promotions', methods=['GET'])
@token_required(roles=['admin', 'empresa'])
def get_promotions_for_restaurant(current_user):
    """Busca todas as promoções de um restaurante."""
    restaurant_id = current_user.get('restaurant_id')
    if current_user['role'] == 'admin':
        restaurant_id = request.args.get('restaurant_id', restaurant_id)

    if not restaurant_id:
        return jsonify({"error": "Restaurante não identificado."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM promotions WHERE restaurant_id = %s ORDER BY created_at DESC", (restaurant_id,))
        promotions = cursor.fetchall()
        
        # Formata datas e decimais para serem compatíveis com JSON
        for promo in promotions:
            if isinstance(promo['start_date'], datetime.date):
                promo['start_date'] = promo['start_date'].isoformat()
            if isinstance(promo['end_date'], datetime.date):
                promo['end_date'] = promo['end_date'].isoformat()
            if isinstance(promo['discount_value'], Decimal):
                promo['discount_value'] = float(promo['discount_value'])

        cursor.close()
        conn.close()
        return jsonify(promotions)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# --- Executar a Aplicação ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)