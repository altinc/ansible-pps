# Phone Provisioning System

Test the app.
```
sudo ufw allow 5000  # to undo: sudo ufw delete allow 5000
source env/bin/activate
python app.py
open http://HOSTNAME:5000
```
If that doesn't work, try running the Flask app with `app.run(debug=True)`

Test gunicorn.
```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Test gunicorn in debug mode.
```
gunicorn --log-level debug --error-logfile error.log \
    --bind 0.0.0.0:5000 wsgi:app
```

Test gunicorn in debug mode binding to socket.
```
gunicorn --workers 3 --log-level deketbug --error-logfile error.log \
    --bind unix:flask-ansible-example.sock -m 007 wsgi:app
```

Run nginx tests.
```
sudo nginx -t
```

Check ports in use.
```
netstat -plnt
```

Check all active connections.
```
netstat -a
```

If need be, kill any processes using a specific port.
```
sudo fuser -k 80/tcp
```

Check facts.
```
ansible webservers -m setup
```

