# frontend_service/app.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = 'DragonGod858'
CORS(app, supports_credentials=True)

# URLs for backend services
USER_SERVICE_URL = 'http://user_service:5001'
CAR_INVENTORY_SERVICE_URL = 'http://car_inventory_service:5002'
BOOKING_SERVICE_URL = 'http://booking_service:5003'

# Home Page
@app.route('/')
def index():
    response = requests.get(f"{CAR_INVENTORY_SERVICE_URL}/cars")
    if response.status_code == 200:
        cars = response.json()
    else:
        cars = []
    return render_template('index.html', cars=cars)

# Register Page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Handle Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(f"{USER_SERVICE_URL}/register", json=payload)
    if response.status_code == 201:
        return redirect(url_for('login_page'))
    else:
        return jsonify({'message': response.json().get('message', 'Registration failed')}), response.status_code

# Login Page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Handle Login with incorrect credentials handling
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(f"{USER_SERVICE_URL}/login", json=payload)
    if response.status_code == 200:
        session['username'] = username
        # Fetch user ID from user_service
        user_response = requests.get(f"{USER_SERVICE_URL}/user", params={'username': username})
        if user_response.status_code == 200:
            user_data = user_response.json()
            session['user_id'] = user_data.get('id')
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        # If credentials are incorrect, return an error message
        error_message = response.json().get('message', 'Login failed')
        return jsonify({'message': error_message}), 401

# Logout
@app.route('/api/logout', methods=['POST'])
def logout():
    response = requests.post(f"{USER_SERVICE_URL}/logout")
    if response.status_code == 200:
        session.pop('username', None)
        session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# Add Car Page
@app.route('/add_car', methods=['GET'])
def add_car_page():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('add_car.html')

# Handle Add Car
@app.route('/api/add_car', methods=['POST'])
def add_car():
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found'}), 400

    make = request.form.get('make')
    model = request.form.get('model')
    year = request.form.get('year')
    price_per_day = request.form.get('price_per_day')
    photo = request.files.get('photo')

    if not all([make, model, year, price_per_day, photo]):
        return jsonify({'message': 'All fields are required'}), 400

    files = {'photo': photo}
    data = {
        'owner_id': user_id,
        'make': make,
        'model': model,
        'year': year,
        'price_per_day': price_per_day
    }

    response = requests.post(f"{CAR_INVENTORY_SERVICE_URL}/add_car", data=data, files=files)
    if response.status_code == 201:
        return jsonify({'message': 'Car added successfully'}), 201
    else:
        return jsonify({'message': response.json().get('message', 'Failed to add car')}), response.status_code

# Book Car Page
@app.route('/book_car/<int:car_id>', methods=['GET'])
def book_car_page(car_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('book_car.html', car_id=car_id)

# Handle Booking Car
@app.route('/api/book_car', methods=['POST'])
def book_car():
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found'}), 400

    data = request.get_json()
    car_id = data.get('car_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not all([car_id, start_date, end_date]):
        return jsonify({'message': 'All fields are required'}), 400

    payload = {
        'user_id': user_id,
        'car_id': car_id,
        'start_date': start_date,
        'end_date': end_date
    }

    response = requests.post(f"{BOOKING_SERVICE_URL}/book_car", json=payload)
    if response.status_code == 201:
        return jsonify({'message': 'Car booked successfully'}), 201
    else:
        return jsonify({'message': response.json().get('message', 'Failed to book car')}), response.status_code

# Serve Uploaded Images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('../car_inventory_service/uploads', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
