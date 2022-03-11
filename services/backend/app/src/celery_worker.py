from celery import Celery

celery = Celery(__name__, backend='redis://redis:6379/0',
                broker="redis://redis:6379/0")
