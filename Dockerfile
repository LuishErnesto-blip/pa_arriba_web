# ============================================
# ETAPA 1 — Genera el CSS de Tailwind (temporal, se descarta al final)
# ============================================
FROM node:20-slim AS tailwind-builder
WORKDIR /build
COPY package.json package-lock.json* ./
RUN npm install
COPY tailwind.config.js ./
COPY core/static/core/src/input.css ./core/static/core/src/input.css
COPY core/templates ./core/templates
COPY blog/templates ./blog/templates
COPY store/templates ./store/templates
COPY termometro/templates ./termometro/templates
RUN npx tailwindcss -i ./core/static/core/src/input.css -o ./core/static/core/tailwind_build.css --minify

# ============================================
# ETAPA 2 — Imagen final de producción (Python, igual que antes)
# ============================================
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ARG CACHE_BUST=1783772096
COPY . /app/
COPY --from=tailwind-builder /build/core/static/core/tailwind_build.css /app/core/static/core/tailwind_build.css
RUN python manage.py collectstatic --noinput
EXPOSE 8080
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn pa_arriba_project.wsgi:application --bind 0.0.0.0:8080"]
# force-rebuild-1780258732
# css-links-1780310075
# force-rebuild-1780576423
# dashboard-crm-1780670720
# btn-dashboard-1780671334
# dashboard-btn-1780672212
# fix-dashboard-1780672822
# fix-dashboard-btn-1780673363
# force-1780673363
# rebuild-1783767030
