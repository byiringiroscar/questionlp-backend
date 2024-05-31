from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime

from .database import Base


class FileUpload(Base):
    __tablename__ = "fileuploads"
    id = Column(Integer, primary_key=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_content = Column(String, nullable=False)
    time_uploaded = Column(TIMESTAMP, default=datetime.utcnow())
    questionanswers = relationship("QuestionAnswer", back_populates="fileupload")



class QuestionAnswer(Base):
    __tablename__ = "questionanswers"
    id = Column(Integer, primary_key=True, nullable=False)
    fileupload_id = Column(Integer, ForeignKey("fileuploads.id"))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    time_uploaded = Column(TIMESTAMP, default=datetime.utcnow())

    fileupload = relationship("FileUpload", back_populates="questionanswers")