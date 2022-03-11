import random
import string
import aiofiles
from .celery_worker import celery
from fastapi.responses import FileResponse, JSONResponse
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8082"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    pdfid = generate_pdfid()

    async with aiofiles.open("/app/uploaded-files/" + pdfid + ".pdf", mode='wb') as f:
        await f.write(contents)
    return pdfid


@app.get("/runocronpdf/{pdfid}")
async def runocronpdf(pdfid):
    task_name = "run_ocr_process_on_pdf"
    task = celery.send_task(task_name, args=[pdfid])
    return JSONResponse({"task_id": task.id, "url": 'localhost:5000/check_task/{}'.format(task.id)})
    # task = run_ocr_process_on_pdf.delay()


@app.get("/ocrstatus/{task_id}")
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


@app.get("/file/{pdfid}", response_class=FileResponse)
async def read_item(pdfid):
    return "/app/uploaded-files/" + pdfid + ".pdf"


def generate_pdfid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
