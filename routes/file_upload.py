from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile
from typing import Optional
from sqlalchemy.orm import Session
from schemas.fileuploads import FileUpload
from sqlalchemy import or_
from starlette.responses import JSONResponse
from database.database import get_db
from database import database, models
from random import randint
from sqlalchemy.sql.expression import text
from utils.cleantext import clean_text
import pymupdf
import os
from utils.langchainsetup import get_text_chunks, get_vector_store, user_input



router = APIRouter(prefix='/question', tags=['QuestionNLP'])


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
        # add in database
        new_file = models.FileUpload(file_name=file.filename, file_content=file_new_content)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        # process documents with gemini and langchain
        text_chunks = get_text_chunks(file_new_content)
        get_vector_store(text_chunks, new_file.id)
        return JSONResponse(content={"response": 'data uploaded successfully'}, status_code=status.HTTP_200_OK)

    except Exception as e:
        # Handle potential errors during processing
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/ask_question")
async def ask_question(question: str, folder_id: Optional[int] = None , db: Session=Depends(get_db)):
    # check if question is not provided or is empty
    if not question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question is required")
    

    folder_document_id = None
    if folder_id:
        file = db.query(models.FileUpload).filter(models.FileUpload.id == folder_id).first()
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found id mismatch")
        folder_document_id = folder_id
    else:
        file = db.query(models.FileUpload).order_by(models.FileUpload.id.desc()).first()
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found please upload some pdf")
        folder_document_id = file.id

    response = user_input(question, folder_document_id)
    # save to database 
    new_question = models.QuestionAnswer(question=question, answer=response, fileupload_id=folder_document_id)
    return {
        "response": response
    }
    



