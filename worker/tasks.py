import asyncio

from celery import Celery
from celery.schedules import crontab
from config.config import config

celery_event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

app: Celery = Celery('celery',
                     broker=f'redis://{config.redis.host}:{config.redis.port}/0',
                     backend=f'redis://{config.redis.host}:{config.redis.port}/0')

app.autodiscover_tasks(['worker.notify'])

app.conf.beat_schedule = {
    "add-every-minute": {
        "task": "worker.notify.test_task",
        "schedule": crontab(minute="*/1"),
    },
}

app.conf.update(timezone="Europe/Moscow")
