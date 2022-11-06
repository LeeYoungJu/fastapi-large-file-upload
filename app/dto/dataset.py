from pydantic import BaseModel


class DatasetBase(BaseModel):
    id: str
    file_name: str
    file_ext: str
    file_size: int
    num_of_rows: int
    num_of_cols: int
    num_of_files: int
    max_rows_in_a_file: int
    col_names: list[str]
    saved_folder_path: str


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(DatasetBase):
    pass
