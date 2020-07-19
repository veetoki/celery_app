# Rectangle Updater

Rectangle Updater is a celery app taking rectangle id to calculate rectangle area and perimeter and update it to the database.

## Installation
Requirements:

You should install docker and docker-compose (at least version 1.23)

Clone the repository
```bash
git clone https://github.com/veetoki/rectangle_updater.git
```

Go into Rectangle Updater directory
```bash
cd celery_app
```
Run
```bash
docker-compose up -d
```

## Usage
##### WARNING
If you have redis server in your local, you should stop it so that the app will run properly.
```bash
/etc/init.d/redis-server stop
```

Run this command to start the app
```bash
docker-compose run app
```
