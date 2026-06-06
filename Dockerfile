# Étape 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .

# Créer un virtual environment et installer les dépendances
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Étape 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances runtime minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier le virtual environment depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Copier le code application
COPY . .

# Définir le PATH
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Exposer le port FastAPI
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
