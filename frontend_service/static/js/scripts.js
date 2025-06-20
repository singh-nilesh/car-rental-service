// frontend_service/static/js/scripts.js

// Helper function to display messages with our new styling
function showMessage(element, isSuccess, message) {
    // Remove any existing alert classes
    element.classList.remove('alert-success', 'alert-danger');
    
    // Add the appropriate class
    element.classList.add(isSuccess ? 'alert-success' : 'alert-danger');
    element.classList.add('alert');
    
    // Set the message
    element.textContent = message;
    
    // Make sure the element is visible
    element.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', () => {
    // Handle Registration
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();

            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            const message = document.getElementById('register-message');

            if (response.status === 201) {
                showMessage(message, true, data.message);
                registerForm.reset();
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                showMessage(message, false, data.message);
            }
        });
    }

    // Handle Login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('login-username').value.trim();
            const password = document.getElementById('login-password').value.trim();

            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            const message = document.getElementById('login-message');

            if (response.status === 200) {
                showMessage(message, true, data.message);
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showMessage(message, false, data.message);
            }
        });
    }

    // Handle Logout
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            const response = await fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();

            if (response.status === 200) {
                alert(data.message);
                window.location.href = '/';
            } else {
                alert('Failed to logout');
            }
        });
    }

    // Handle Add Car
    const addCarForm = document.getElementById('add-car-form');
    if (addCarForm) {
        addCarForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addCarForm);

            const response = await fetch('/api/add_car', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            const message = document.getElementById('add-car-message');

            if (response.status === 201) {
                showMessage(message, true, data.message);
                addCarForm.reset();
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else {
                showMessage(message, false, data.message);
            }
        });
    }

    // Handle Book Car
    const bookCarForm = document.getElementById('book-car-form');
    if (bookCarForm) {
        bookCarForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const car_id = document.getElementById('car_id').value;
            const start_date = document.getElementById('start_date').value;
            const end_date = document.getElementById('end_date').value;

            const response = await fetch('/api/book_car', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ car_id, start_date, end_date }),
            });

            const data = await response.json();
            const message = document.getElementById('book-car-message');

            if (response.status === 201) {
                showMessage(message, true, data.message);
                bookCarForm.reset();
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else {
                showMessage(message, false, data.message);
            }
        });
    }

    // Handle Book Now Buttons on Home Page
    const bookButtons = document.querySelectorAll('.book-button');
    bookButtons.forEach(button => {
        button.addEventListener('click', () => {
            const carId = button.getAttribute('data-car-id');
            window.location.href = `/book_car/${carId}`;
        });
    });
});
