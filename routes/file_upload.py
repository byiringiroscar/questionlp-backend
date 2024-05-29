from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session
from schemas.fileuploads import FileUpload
from sqlalchemy import or_
from starlette.responses import JSONResponse
from database.database import get_db
from database import database, models
from random import randint
from sqlalchemy.sql.expression import text
from database.config import settings
import random
import string



router = APIRouter(prefix='/question', tags=['QuestionNLP'])


@router.post("/file_upload", response_model=FileUpload)
async def file_upload_display(file_upload: FileUpload, db: Session=Depends(get_db)):
    return {
        'success': 'file_uploaded'
    }



