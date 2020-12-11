source python-env/bin/activate
pip3 install -r requirements.txt
python3 qurry_api/manage.py makemigrations
python3 qurry_api/manage.py migrate