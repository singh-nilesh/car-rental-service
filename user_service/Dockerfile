# user_service/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN pip install flask flask-cors bcrypt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
