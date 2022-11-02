import os
import math
import glob
import shutil

from fastapi import Request

from app.utils.file_path_utils import get_file_ext, get_file_name_only
from app.consts import PATH, UPLOAD
from app.utils.common_utils import decode_base64
from app.service.cloud_upload_service import CloudUploadService
from app.dao import UploadHeader


class UploadTabularService:

    def __init__(self, meta_data: UploadHeader):
        self.file_name = meta_data.file_name
        self.file_name_only = get_file_name_only(meta_data.file_name)
        self.file_size = meta_data.file_size
        self.cur_chunk_idx = meta_data.cur_chunk_idx
        self.total_chunks = meta_data.total_chunks
        self.cur_row_idx = int(meta_data.cur_row_idx)

        self.is_first_chunk = int(self.cur_chunk_idx) == 0
        self.is_last_chunk = int(self.cur_chunk_idx) == int(meta_data.total_chunks) - 1

        self.ext = get_file_ext(self.file_name)

        self.tmp_path = os.path.join(PATH.APP_DIR, 'tmp', self.file_name_only)
        if self.is_first_chunk:
            if not os.path.isdir(self.tmp_path):
                os.makedirs(self.tmp_path)

        self.file_count = math.ceil((self.cur_row_idx+1) / UPLOAD.NUM_OF_ROWS_IN_A_FILE)

        self.chunk = b''

    def is_first(self):
        return self.is_first_chunk

    def is_last(self):
        return self.is_last_chunk

    def write_file_locally(self, lines: list[bytes], file_count):
        file_name = f'{self.file_name_only}{file_count}.{self.ext}'
        upload_path = os.path.join(self.tmp_path, file_name)
        f = open(upload_path, 'ab')
        f.write(b'\n'.join(lines))
        f.close()

    async def upload_chunk(self, request: Request):
        # async for chunk in request.stream():
        #     self.chunk += chunk
        self.chunk = await request.body()

        decoded_chunk = decode_base64(self.chunk)
        num_of_rows_in_chunk = decoded_chunk.count(b'\n')
        sum_of_rows = self.cur_row_idx + num_of_rows_in_chunk
        new_file_count = math.ceil((sum_of_rows+1) / UPLOAD.NUM_OF_ROWS_IN_A_FILE)
        origin_line = 0
        for i in range(self.file_count, new_file_count+1):
            required_new_lines = (UPLOAD.NUM_OF_ROWS_IN_A_FILE * i) - self.cur_row_idx
            new_lines = decoded_chunk.split(b'\n')[origin_line:required_new_lines]
            origin_line = required_new_lines
            self.write_file_locally(new_lines, i)

        if self.is_last():
            cloud_upload_service = CloudUploadService()
            for csv_file_path in glob.glob(os.path.join(self.tmp_path, '*')):
                _, s3_object_name = os.path.split(csv_file_path)
                cloud_upload_service.upload(csv_file_path, 'yjlee', f'{self.file_name_only}/{s3_object_name}')

            shutil.rmtree(self.tmp_path)

        self.cur_row_idx += num_of_rows_in_chunk
        print(self.cur_row_idx)

        return self.cur_row_idx


