ps ax| grep "manage.py"| awk '{print $1}' | xargs kill
ps ax| grep "python3" | grep "worker" | awk '{print $1}' | xargs kill
ps ax| grep "python3" | grep "beat" | awk '{print $1}' | xargs kill
ps ax| grep "redis-server" | awk '{print $1}' | xargs kill