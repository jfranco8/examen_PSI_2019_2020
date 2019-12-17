dropdb -U alumnodb examen
createdb -U alumnodb examen

python manage.py makemigrations aplicacion
python manage.py migrate

python manage.py createsuperuser

python poblar.py
