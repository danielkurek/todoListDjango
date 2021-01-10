ToDo list app in Django
## Features
- [x] Tags
- [x] Filter tasks
- [x] Repeating tasks
- [ ] Remainder
- [x] Multiple lists
- [ ] Multiple users
- [ ] Sharing lists
- [ ] JS frontend

## Instalation
1) Clone this repository and go to repository folder
```
    git clone https://github.com/danielkurek/todoListDjango
    cd todoListDjango
```
2) Install required packages

    `python -m pip install -r requirements.txt`
3) Initialize database

    `python manage.py migrate`
4) Start server

    `python manage.py runserver`

## Create admin account (optional)

If you want to use admin console, you have to setup superuser:

    python manage.py createsuperuser
Enter your desired username and press enter.

    Username: admin
Then enter your desired email address:

    Email address: admin@example.com
Then you will be prompted to enter your desired password:
```
Password: ********
Password (again): ********
Superuser created successfully.
``` 
