from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'group9'

USER_SERVICE_URL = 'http://user_service:5001'
CAR_INVENTORY_SERVICE_URL = 'http://car_inventory_service:5002'
BOOKING_SERVICE_URL = 'http://booking_service:5003'

@app.route('/')
def home():
    response = requests.get(f'{CAR_INVENTORY_SERVICE_URL}/cars')
    cars = response.json()
    return render_template('index.html', cars=cars)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{USER_SERVICE_URL}/register', json={'username': username, 'password': password})
        if response.status_code == 201:
            return redirect(url_for('login'))
        return "Registration failed", 400
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{USER_SERVICE_URL}/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            session['user_id'] = response.json()['user_id']
            return redirect(url_for('all_cars'))
        return "Login failed", 400
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/all_cars')
def all_cars():
    response = requests.get(f'{CAR_INVENTORY_SERVICE_URL}/cars')
    cars = response.json()
    return render_template('all_cars.html', cars=cars)

@app.route('/my_cars')
def my_cars():
    user_id = session.get('user_id')
    response = requests.get(f'{CAR_INVENTORY_SERVICE_URL}/user_cars/{user_id}')
    user_cars = response.json()
    return render_template('my_cars.html', cars=user_cars)

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price_per_day = request.form['price_per_day']
        photo = request.files['photo']

        # Prepare data to send to the backend
        data = {'owner_id': session['user_id'], 'make': make, 'model': model, 'year': year, 'price_per_day': price_per_day}
        files = {'photo': photo}

        # Submit the car details to the backend
        response = requests.post(f'{CAR_INVENTORY_SERVICE_URL}/add_car', data=data, files=files)

        # Log the raw response (status code, headers, content)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Raw Response Content: {response.text}")  # Logs raw text response

        # Check the response status code and handle accordingly
        if response.status_code == 201:
            return redirect(url_for('all_cars'))
        else:
            # Log error message to the console, if available in JSON
            try:
                error_message = response.json()
                print(f"Error: {error_message}")
            except ValueError:  # Catch the case where response is not JSON
                print("Response is not JSON. Raw response:", response.text)
            
            # Optionally, handle the non-JSON error message 

    return render_template('add_car.html')



@app.route('/book_car/<int:car_id>', methods=['POST'])
def book_car(car_id):
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    data = {'user_id': session['user_id'], 'car_id': car_id, 'start_date': start_date, 'end_date': end_date}
    requests.post(f'{BOOKING_SERVICE_URL}/book_car', json=data)
    return redirect(url_for('success_booking'))

@app.route('/success_booking')
def success_booking():
    return render_template('success_booking.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
