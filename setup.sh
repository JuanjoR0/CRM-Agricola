#!/usr/bin/env bash

echo "📦 Ejecutando makemigrations..."
python manage.py makemigrations --noinput
echo "✅ Makemigrations hecho"

echo "📦 Ejecutando migrate..."
python manage.py migrate --noinput
echo "✅ Migraciones aplicadas"

echo "🛡️  Creando superusuario si no existe..."
python manage.py shell < init_superuser.py

echo "🚀 Lanzando Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000
