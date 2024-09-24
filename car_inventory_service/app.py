# car_inventory_service/app.py

from flask import Flask, request, jsonify
import sqlite3
from database import init_db
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

init_db()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

DATABASE = 'database.db'

# Add Car
@app.route('/add_car', methods=['POST'])
def add_car():
    if 'photo' not in request.files:
        return jsonify({'message': 'No photo uploaded'}), 400

    photo = request.files['photo']

    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return jsonify({'message': 'Invalid file type'}), 400

    data = request.form
    owner_id = data.get('owner_id')  # This should come from the authenticated user
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    price_per_day = data.get('price_per_day')

    if not all([owner_id, make, model, year, price_per_day]):
        return jsonify({'message': 'All fields are required'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO cars (owner_id, make, model, year, price_per_day, photo)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   (owner_id, make, model, int(year), float(price_per_day), filename))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Car added successfully'}), 201

# Update Car
@app.route('/update_car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.json
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    price_per_day = data.get('price_per_day')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""UPDATE cars SET make = ?, model = ?, year = ?, price_per_day = ?
                      WHERE id = ?""",
                   (make, model, year, price_per_day, car_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Car updated successfully'}), 200

# Delete Car
@app.route('/delete_car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Car deleted successfully'}), 200

# Get All Cars
@app.route('/cars', methods=['GET'])
def get_cars():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()

    car_list = []
    for car in cars:
        car_data = {
            'id': car[0],
            'owner_id': car[1],
            'make': car[2],
            'model': car[3],
            'year': car[4],
            'price_per_day': car[5],
            'photo': car[6]
        }
        car_list.append(car_data)

    return jsonify(car_list), 200

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0', port=5002, debug=True)
