from pydantic import BaseModel
from typing import Optional



class FileUpload(BaseModel):
    file_name: str
    file_content: str
    time_uploaded: Optional[str] = None
    id: Optional[int] = None
    class Config:
        orm_mode = True