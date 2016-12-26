
pkill gunicorn;
gunicorn h5music.wsgi --worker-class=gevent -b 127.0.0.1:9000 -D
