from sqlalchemy.orm import Session

from app.repo.base import RepoBase
from app.models import Dataset
from app.dto import DatasetCreate, DatasetUpdate


class DatasetRepo(RepoBase[Dataset, DatasetCreate, DatasetUpdate]):

    def create(self, db: Session, *, obj_in: DatasetCreate) -> Dataset:
        db_obj = Dataset(
            id = obj_in.id,
            file_name = obj_in.file_name,
            file_ext = obj_in.file_ext,
            file_size = obj_in.file_size,
            num_of_rows = obj_in.num_of_rows,
            num_of_cols = obj_in.num_of_cols,
            num_of_files = obj_in.num_of_files,
            max_rows_in_a_file = obj_in.max_rows_in_a_file,
            col_names = obj_in.col_names,
            saved_folder_path = obj_in.saved_folder_path
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


dataset_repo = DatasetRepo(Dataset)
