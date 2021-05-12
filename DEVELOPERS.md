# Developer Setup

## Steps to setup
1. Clone the repository by running the following command in the terminal :

   ```shell
   $ git clone https://github.com/Beta-Persei/vaccination-slot-notifier.git
   ```


2. Create a virtual environment and activate it.

   ```shell
   $ python -m venv env
   $ source env/bin/activate (Linux)
   $ env\Scripts\activate (Windows)
   ```

4. Install dependencies by running the following command:
   ```shell
   $ pip install -r requirements.txt
   ```
5. Create a .env file using the .env.sample and add the required values

6. Run the Django standard runserver steps:
   ```shell
   $ python manage.py migrate
   $ python manage.py runserver
   ```
   Your website will be up and running at http://localhost:8000

## Redis
Redis is used as a broker for celery.
1. Install
   ```shell
   $ sudo apt install redis-server
   ```
2. Test
   ```shell
   $ redis-cli ping
   PONG
   ```      

## Celery worker
Celery worker is used to send mails and other blocking tasks asynchronously.
```shell
celery -A vaccination_slot_notifier worker -l DEBUG
```

## Celery beat
Used to run periodic tasks
```shell
celery -A vaccination_slot_notifier beat -l DEBUG
```
