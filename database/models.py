from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime

from .database import base


class FileUpload(base):
    __tablename__ = "fileuploads"
    id = Column(Integer, primary_key=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_content = Column(String, nullable=False)
    time_uploaded = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)