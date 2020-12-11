source python-env/bin/activate
python3 qurry_api/manage.py flush
python3 qurry_api/manage.py makemigrations
python3 qurry_api/manage.py migrate
python3 qurry_api/manage.py loaddata reocrds.json
python3 qurry_api/manage.py shell -c "from users.models import User; User.objects.create_superuser('admin@hpi.de', 'admin', 'admin')"
