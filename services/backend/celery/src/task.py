from .celery_worker import celery
from .ocrengine import recognize


@celery.task(name="run_ocr_process_on_pdf", bind=True)
def run_ocr_process_on_pdf(self, pdfid):
    return recognize(pdfid)
