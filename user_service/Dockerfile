# user_service/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask Flask-Login Flask-Bcrypt Flask-Cors

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
