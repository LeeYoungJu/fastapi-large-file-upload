import uuid
from sqlalchemy import Boolean, Column, Integer, String, JSON

from app.db.base_class import Base


class Dataset(Base):
    id = Column(String(120), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String(200))
    file_ext = Column(String(10))
    file_size = Column(Integer)
    num_of_rows = Column(Integer)
    num_of_cols = Column(Integer)
    num_of_files = Column(Integer)
    num_of_rows_in_a_file = Column(Integer)
    col_names = Column(JSON)
    saved_folder_path = Column(String(500))
