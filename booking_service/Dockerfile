# booking_service/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask Flask-Cors

COPY . .

EXPOSE 5003

CMD ["python", "app.py"]
