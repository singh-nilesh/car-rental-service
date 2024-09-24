# booking_service/app.py

from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

DATABASE = 'database.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        car_id INTEGER NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(car_id) REFERENCES cars(id)
                      )''')
    conn.commit()
    conn.close()

init_db()

# Book Car
@app.route('/book_car', methods=['POST'])
def book_car():
    data = request.json
    user_id = data.get('user_id')  # Should come from authenticated user
    car_id = data.get('car_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not all([user_id, car_id, start_date, end_date]):
        return jsonify({'message': 'All fields are required'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO bookings (user_id, car_id, start_date, end_date)
                      VALUES (?, ?, ?, ?)""",
                   (user_id, car_id, start_date, end_date))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Car booked successfully'}), 201

# Get Bookings for a User
@app.route('/bookings/<int:user_id>', methods=['GET'])
def get_bookings(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
    bookings = cursor.fetchall()
    conn.close()

    booking_list = []
    for booking in bookings:
        booking_data = {
            'id': booking[0],
            'user_id': booking[1],
            'car_id': booking[2],
            'start_date': booking[3],
            'end_date': booking[4]
        }
        booking_list.append(booking_data)

    return jsonify(booking_list), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
