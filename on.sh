python3 manage.py runserver 0.0.0.0:80 &
./redis-stable/src/redis-server &
python3 -m celery -A CouncilTest worker -l info &
python3 -m celery -A CouncilTest beat -l info &
curl -s 'http://ddns.dnszi.com/set.html?user=goraegori&auth=a0vr3a8b3s&domain=ssusw.com&record='