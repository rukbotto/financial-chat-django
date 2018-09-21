# Financial Chat Django

A simple chat application powered by *Django*.

## Installation

Install *PostgreSQL* and *Git*:

```
# On MacOS
$ brew install postgresql git

# On Debian GNU/Linux
$ sudo apt install postgresql git
```

Install `virtualenv` or `virtualenvwrapper`:

```
# Install virtualenv
$ sudo pip install virtualenv

# Or virtualenvwrapper
$ sudo pip install virtualenvwrapper
```

Clone this repository:

```
$ git clone https://github.com/rukbotto/financial-chat-django ~/financial-chat-django
```

Create a virtualenv for installing all dependencies:

```
# Using virtualenv
$ virtualenv ~/.virtualenvs/financial-chat-django --python=python3

# Or using virtualenvwrapper
$ mkvirtualenv financial-chat-django --python=python3
```

Activate the newly created virtualenv:

```
# Using virtualenv
$ source ~/.virtualenvs/financial-chat-django/bin/activate

# Or using virtualenvwrapper
$ workon financial-chat-django
```

Install all dependencies:

```
(financial-chat-django) $ cd ~/financial-chat-django
(financial-chat-django) $ pip install -r requirements.txt
```

## Database configuration

Create a new PostgreSQL role:

```
(financial-chat-django) $ psql postgres
postgres=# CREATE ROLE financial_chat_django WITH LOGIN PASSWORD 'strong_password_here';
postgres=# ALTER ROLE financial_chat_django CREATEDB;
postgres=# \q
```

Then create the database using the recently created user:

```
(financial-chat-django) $ psql postgres -U financial_chat_django
postgres=> CREATE DATABASE financial_chat_django;
```

Finally grant permissions:

```
postgres=> GRANT ALL PRIVILEGES ON DATABASE financial_chat_django TO financial_chat_django;
postgres=> \q
```

## Django configuration

Create a local configuration file:

```
(financial-chat-django) $ touch financial_chat_django/local_settings.py
```

And add the following lines of code in order to configure local development settings:

```python
SECRET_KEY='secret_key_here'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'financial_chat_django',
        'USER': 'financial_chat_django',
        'PASSWORD': 'strong_password_here',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

The secret key can be generated by *Django* using the interactive *Python* shell:

```
(financial-chat-django) $ python
Python 3.7.0 (default, Jun 29 2018, 20:13:13)
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
>>> '3z^w%y!...'
```

Copy the generated secret key and paste it into the `SECRET_KEY` setting in the local configuration file.

## Usage

Run database migrations:

```
(financial-chat-django) $ python manage.py migrate
```

Run the local development server:

```
(financial-chat-django) $ python manage.py runserver
```
