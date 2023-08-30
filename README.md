# Numble

![Static Badge](https://img.shields.io/badge/python-3.11-blue?logo=python)
![Static Badge](https://img.shields.io/badge/pre--commit-enabled-orange?logo=pre-commit)

A casual arithmetic puzzle game. Play today's game at [numble.fly.dev](https://numble.fly.dev/)

## Developer Setup
This project uses django, python3.11, and bootstrap 5.

To set up the development environment, from the root directory run:
```
source setup.sh
```

To start a local server, from the root directory run:
```
python django-app/manage.py runserver
```


## Deployment
Numble is hosted and deployed with [fly.io](https://fly.io/)

To deploy a new version, replace <django-secret-key> with the key value and run:
```
fly deploy --build-arg SECRET_KEY=<django-secret-key> --build-arg DJANGO_SETTINGS_MODULE=django-app.prod_settings
```


## Contact
Email: taliaben-naim2025@u.northwestern.edu

LinkedIn: [www.linkedin.com/in/talia-ben-naim](www.linkedin.com/in/talia-ben-naim)
