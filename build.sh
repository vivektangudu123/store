set -o errexit

pip install -r requirements.txt
python manage.py migrate
echo -e 'Starting importing of data'
# python manage.py import_data
echo -e 'Importing of data is complete'
