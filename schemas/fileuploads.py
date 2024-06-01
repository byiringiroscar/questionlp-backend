from pydantic import BaseModel
from typing import Optional



class FileUpload(BaseModel):
    file_name: str
    file_content: str

    class Config:
        orm_mode = True


class QuestionRequest(BaseModel):
    question: str
    folder_id: Optional[int] = None
