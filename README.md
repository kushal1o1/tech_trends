# tech_trends
python manage.py runserver
redis-server
celery -A tech_trends beat --loglevel=info
celery -A tech_trends worker --pool=solo -l info