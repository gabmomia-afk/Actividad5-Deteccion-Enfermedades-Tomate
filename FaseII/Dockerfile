
FROM python:3.11-slim

WORKDIR /app

COPY FaseII/requirements-docker.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY FaseII/Backend /app/FaseII/Backend
COPY FaseII/Frontend /app/FaseII/Frontend

EXPOSE 8000

CMD ["uvicorn", "FaseII.Backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
