from celery import Celery

celery = Celery(__name__, backend='redis://ocrify-redis-1:6379/0',
                broker="redis://ocrify-redis-1:6379/0")
