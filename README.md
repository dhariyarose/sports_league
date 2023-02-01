
How to run: 

Do the following steps,

git clone https://github.com/dhariyarose/sports_league.git
cd sports_league/
virtualenv env_name
source env_name/bin/activate
pip3 install -r requirements.txt
mkdir static
mkdir media
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python manage.py runserver