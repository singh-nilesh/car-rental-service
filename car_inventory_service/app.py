from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app, supports_credentials=True)

DATABASE = 'database.db'

# Initialize database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            owner_id INTEGER NOT NULL,
                            make TEXT NOT NULL,
                            model TEXT NOT NULL,
                            year INTEGER NOT NULL,
                            price_per_day REAL NOT NULL,
                            photo BLOB,
                            FOREIGN KEY(owner_id) REFERENCES users(id)
                        )''')
        conn.commit()

init_db()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# add Cars
@app.route('/add_car', methods=['POST'])
def add_car():
    try:
        # Check if the photo file is in the request
        if 'photo' not in request.files:
            return jsonify({'message': 'No photo uploaded'}), 400

        photo = request.files['photo']

        # Check if file is allowed
        if photo and allowed_file(photo.filename):
            photo_data = photo.read()  # Read the photo data
        else:
            return jsonify({'message': 'Invalid file type'}), 400

        data = request.form
        owner_id = data.get('owner_id')
        make = data.get('make')
        model = data.get('model')
        year = data.get('year')
        price_per_day = data.get('price_per_day')

        if not all([owner_id, make, model, year, price_per_day]):
            return jsonify({'message': 'All fields are required'}), 400

        # Insert car details into the database
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO cars (owner_id, make, model, year, price_per_day, photo)
                              VALUES (?, ?, ?, ?, ?, ?)""",
                           (owner_id, make, model, int(year), float(price_per_day), photo_data))
            conn.commit()

        return jsonify({'message': 'Car added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

# Update Car
@app.route('/update_car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    try:
        data = request.json
        make = data.get('make')
        model = data.get('model')
        year = data.get('year')
        price_per_day = data.get('price_per_day')

        if not all([make, model, year, price_per_day]):
            return jsonify({'message': 'All fields are required'}), 400

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE cars SET make = ?, model = ?, year = ?, price_per_day = ?
                              WHERE id = ?""",
                           (make, model, int(year), float(price_per_day), car_id))
            conn.commit()

        return jsonify({'message': 'Car updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete Car
@app.route('/delete_car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
            conn.commit()
        return jsonify({'message': 'Car deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get All Cars
@app.route('/cars', methods=['GET'])
def get_cars():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cars")
            cars = cursor.fetchall()

        car_list = []
        for car in cars:
            car_data = {
                'id': car[0],
                'owner_id': car[1],
                'make': car[2],
                'model': car[3],
                'year': car[4],
                'price_per_day': car[5],
                'photo': base64.b64encode(car[6]).decode('utf-8') if car[6] else None  # Convert BLOB to base64
            }
            car_list.append(car_data)

        return jsonify(car_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Cars Registered by a Specific User
@app.route('/user_cars/<int:user_id>', methods=['GET'])
def get_users_cars(user_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cars WHERE owner_id = ?", (user_id,))
            cars = cursor.fetchall()

        car_list = []
        for car in cars:
            car_data = {
                'id': car[0],
                'owner_id': car[1],
                'make': car[2],
                'model': car[3],
                'year': car[4],
                'price_per_day': car[5],
                'photo': base64.b64encode(car[6]).decode('utf-8') if car[6] else None  # Convert BLOB to base64
            }
            car_list.append(car_data)

        return jsonify(car_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
