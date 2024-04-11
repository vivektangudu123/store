set -o errexit

pip install -r requirements.txt
python manage.py migrate
# python manage.py import_data
echo -e 'Importing of data is complete'
