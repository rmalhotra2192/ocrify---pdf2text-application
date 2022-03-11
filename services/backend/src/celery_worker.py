from .ocrengine import recognize
from celery import Celery


celery = Celery(__name__, backend='redis://localhost:6379/0',
                broker="redis://localhost:6379/0")


@celery.task(name="run_ocr_process_on_pdf")
def run_ocr_process_on_pdf(pdfid):
    return recognize(pdfid)
