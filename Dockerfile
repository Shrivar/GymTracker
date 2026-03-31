FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV SECRET_KEY=dummy-build-only-secret-key

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD exec gunicorn --bind :$PORT --workers 2 --timeout 60 config.wsgi:application

