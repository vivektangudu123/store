set -o errexit

pip3 install -r requirements.txt
python3 manage.py migrate
# python manage.py import_data
echo -e 'Importing of data is complete'
