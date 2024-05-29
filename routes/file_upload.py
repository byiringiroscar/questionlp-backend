from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session
from schemas.fileuploads import FileUpload
from sqlalchemy import or_
from starlette.responses import JSONResponse
from database.database import get_db
from database import database, models
from random import randint
from sqlalchemy.sql.expression import text
import random
import string
import json



router = APIRouter(prefix='/question', tags=['QuestionNLP'])


@router.post("/file_upload")
async def file_upload_display(file: UploadFile, db: Session=Depends(get_db)):
    data = json.loads(file.file.read())
    # file_name = file_upload.file_name
    # file_content = file_upload.file_content
    # db_file = models.FileUpload(file_name=file_name, file_content=file_content)
    # db.add(db_file)
    # db.commit()
    # db.refresh(db_file)

    return {
        'success': 'file_uploaded',
        'content': data,
        'file_name': file.filename
    }



