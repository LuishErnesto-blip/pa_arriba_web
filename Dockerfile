# Imagen base oficial de Python
FROM python:3.12-slim

# Evita archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt /app/

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Puerto que usa Cloud Run
EXPOSE 8080

# Comando de arranque
CMD ["sh", "-c", "python manage.py migrate --run-syncdb && gunicorn pa_arriba_project.wsgi:application --bind 0.0.0.0:8080"]