import os
import math
import glob
import shutil

from fastapi import Request
from sqlalchemy.orm import Session

from app.utils.file_path_utils import get_file_ext, get_file_name_only
from app.consts import PATH, UPLOAD
from app.utils.common_utils import decode_base64
from app.service.cloud_upload_service import CloudUploadService
from app.dto import TabularUploadHeader
from app.dto import DatasetCreate
from app.repo import dataset_repo


class UploadTabularService:

    def __init__(self, db: Session, meta_data: TabularUploadHeader):
        self.db = db
        self.file_name = meta_data.file_name
        self.file_uuid = meta_data.file_uuid
        self.file_name_only = get_file_name_only(meta_data.file_name)
        self.file_name_uuid = f'{meta_data.file_uuid}{self.file_name_only}'
        self.ext = get_file_ext(meta_data.file_name)
        self.file_size = meta_data.file_size
        self.cur_chunk_idx = meta_data.cur_chunk_idx
        self.total_chunks = meta_data.total_chunks
        self.cur_row_idx = int(meta_data.cur_row_idx)
        self.first_col_names: str = meta_data.first_col_names

        self.is_first_chunk = int(self.cur_chunk_idx) == 0
        self.is_last_chunk = int(self.cur_chunk_idx) == int(meta_data.total_chunks) - 1

        self.tmp_path = os.path.join(PATH.APP_DIR, 'tmp', self.file_name_uuid)
        if self.is_first_chunk:
            if not os.path.isdir(self.tmp_path):
                os.makedirs(self.tmp_path)

        self.file_count = math.ceil((self.cur_row_idx+1) / UPLOAD.NUM_OF_ROWS_IN_A_FILE)

        self.chunk = b''

    def make_dataset_dto(self):
        first_col_name_list = self.first_col_names.replace('\r', '').split(',')
        return DatasetCreate(
            id=self.file_uuid,
            file_name=self.file_name_only,
            file_ext=self.ext,
            file_size=self.file_size,
            num_of_rows=self.cur_row_idx + 1,
            num_of_cols=len(first_col_name_list),
            num_of_files=self.file_count,
            num_of_rows_in_a_file=UPLOAD.NUM_OF_ROWS_IN_A_FILE,
            col_names=first_col_name_list,
            saved_folder_path=self.file_name_uuid
        )

    def is_first(self) -> bool:
        return self.is_first_chunk

    def is_last(self) -> bool:
        return self.is_last_chunk

    def __get_first_col_names(self, decoded_chunk: bytes) -> str:
        return (decoded_chunk.split(b'\n')[0]).decode()

    def __remove_first_col(self, decoded_chunk: bytes) -> bytes:
        return b'\n'.join(decoded_chunk.split(b'\n')[1:])

    def __insert_col_names(self, lines: list, first_col_names):
        lines.insert(0, first_col_names)

    def __upload_completed_file_to_cloud(self, prev_file_path):
        if os.path.exists(prev_file_path):
            self.__upload_a_file_to_cloud(prev_file_path)
            os.remove(prev_file_path)

    def __write_by_file_count(self, decoded_chunk: bytes, start: int, end: int) -> None:
        origin_line = 0
        for i in range(start, end):
            required_new_line = (UPLOAD.NUM_OF_ROWS_IN_A_FILE * i) - self.cur_row_idx
            print(f'{origin_line}:{required_new_line}')
            new_lines = decoded_chunk.split(b'\n')[origin_line:required_new_line]
            origin_line = required_new_line

            file_name = f'{self.file_name_only}{i}.{self.ext}'
            if (self.cur_row_idx + origin_line) % UPLOAD.NUM_OF_ROWS_IN_A_FILE == 0:
                # self.__insert_col_names(new_lines, self.first_col_names.encode())
                prev_file_path = os.path.join(self.tmp_path, f'{self.file_name_only}{i - 1}.{self.ext}')
                self.__upload_completed_file_to_cloud(prev_file_path)

            self.__write_file_local(file_name, new_lines)

    def __write_file_local(self, file_name: str, lines: list[bytes]) -> None:
        upload_path = os.path.join(self.tmp_path, file_name)
        is_first = False
        if not os.path.isfile(upload_path):
            is_first = True
        f = open(upload_path, 'ab')
        if is_first:
            f.write(self.first_col_names.encode() + b'\n')
        f.write(b'\n'.join(lines))
        f.close()

    def __upload_a_file_to_cloud(self, csv_file_path):
        _, s3_object_name = os.path.split(csv_file_path)
        CloudUploadService().upload(csv_file_path, 'yjlee', f'{self.file_name_uuid}/{s3_object_name}')

    def __flush_to_cloud(self):
        for csv_file_path in glob.glob(os.path.join(self.tmp_path, '*')):
            self.__upload_a_file_to_cloud(csv_file_path)

    async def upload_chunk(self, request: Request):
        # async for chunk in request.stream():
        #     self.chunk += chunk
        self.chunk = await request.body()
        decoded_chunk = decode_base64(self.chunk)

        if self.is_first():
            self.first_col_names = self.__get_first_col_names(decoded_chunk)
            decoded_chunk = self.__remove_first_col(decoded_chunk)

        num_of_rows_in_chunk = decoded_chunk.count(b'\n')
        sum_of_rows = self.cur_row_idx + num_of_rows_in_chunk
        new_file_count = math.ceil((sum_of_rows+1) / UPLOAD.NUM_OF_ROWS_IN_A_FILE)

        self.__write_by_file_count(decoded_chunk, self.file_count, new_file_count+1)

        self.cur_row_idx += num_of_rows_in_chunk
        print(self.cur_row_idx)

        if self.is_last():
            self.__flush_to_cloud()
            shutil.rmtree(self.tmp_path)
            dataset_repo.create(db=self.db, obj_in=self.make_dataset_dto())

        return {
            'cur_row_idx': self.cur_row_idx,
            'first_col_names': self.first_col_names,
        }
