# car_inventory_service/Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask Flask-Cors Werkzeug

COPY . .

EXPOSE 5002

CMD ["python", "app.py"]
