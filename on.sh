python3 manage.py runserver 0.0.0.0:8000 &
./redis-5.0.4/src/redis-server &
python3 -m celery -A CouncilTest worker -l info &
python3 -m celery -A CouncilTest beat -l info &