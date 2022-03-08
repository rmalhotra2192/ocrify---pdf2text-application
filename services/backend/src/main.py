import random
import string
import aiofiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    pdfid = generate_pdfid()

    async with aiofiles.open("../uploaded-files/" + pdfid + ".pdf", mode='wb') as f:
        await f.write(contents)
    return pdfid


@app.get("/file/{pdfid}", response_class=FileResponse)
async def read_item(pdfid):
    return "../uploaded-files/" + pdfid + ".pdf"


def generate_pdfid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
