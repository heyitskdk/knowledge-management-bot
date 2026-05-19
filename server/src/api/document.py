from fastapi import APIRouter, File, UploadFile
from typing import Annotated

router = APIRouter(tags=["Knowledge"])

FileUpload = Annotated[UploadFile, File()]

@router.post("/ingest")
async def ingest(file: FileUpload):
    print(file.content_type)
    pass