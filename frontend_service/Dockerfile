# frontend_service/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask requests

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
