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
import pymupdf
import os
import re



router = APIRouter(prefix='/question', tags=['QuestionNLP'])


def clean_text(text):
    # Remove multiple newlines (\n)
    text = text.replace('\n', " ")

    # Remove form feed (\f) characters
    text = re.sub(r"\f", "", text)

    # Remove extra spaces at the beginning and end
    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    return text


@router.post("/file_upload")
async def file_upload_display(file: UploadFile, db: Session=Depends(get_db)):
    # Validate file type (optional)
    if not file.content_type.startswith('application/pdf'):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Only PDF files are allowed.')
    
    random_number = randint(1000, 9999)
    filename = f"temp_pdf_{random_number}.pdf"
    # Save the uploaded file temporarily (optional, adjust as needed)
    file_content = await file.read()
    with open(filename, "wb") as buffer:
        buffer.write(file_content)
    
    try:                               
        text_content = ""
        doc = pymupdf.open(filename)
        for page in doc:
            text = page.get_text().encode("utf8")
            text_content += text.decode("utf-8")

        doc.close()

        # Clean up temporary file (optional)
        os.remove(filename)

        # Return the extracted text
        file_new_content = clean_text(text_content)
        return JSONResponse(content={"text_content": file_new_content}, status_code=status.HTTP_200_OK)

    except Exception as e:
        # Handle potential errors during processing
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    



