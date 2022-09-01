python -m venv .
CALL ."/Scripts/activate"
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations
python manage.py runserver

