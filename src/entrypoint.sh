#All the prerequisites needed to bring up the django service
python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate && python manage.py test && hypercorn --bind '0.0.0.0:8000' src.asgi:application --reload