import os

from app.consts import UPLOAD
from app.utils.file_path_utils import get_file_ext, get_file_name_only


class TabularToCloudService:

    def __init__(self, file_name, folder_path):
        self.file_name = file_name
        self.file_name_only = get_file_name_only(file_name)
        self.ext = get_file_ext(file_name)
        self.folder_path = folder_path

    def __write(self, contents: bytes, file_cnt: int):
        print(file_cnt)
        file_path = os.path.join(self.folder_path, f'{self.file_name_only}{file_cnt}.{self.ext}')
        with open(file_path, "wb") as wf:
            wf.write(contents)

    def __write_split_file(self, file_cnt: int, first_col_names: bytes, contents_in_file: bytes):
        contents_in_file = first_col_names + contents_in_file
        self.__write(contents_in_file, file_cnt)

    def upload_to_cloud(self):
        first_col_names = b''
        contents_in_file = b''
        file_cnt = 0
        file_path = os.path.join(self.folder_path, self.file_name)
        with open(file_path, "rb") as f:
            for i, line in enumerate(f):
                if i == 0:
                    first_col_names = line
                    continue

                contents_in_file += line
                if i % UPLOAD.MAX_ROWS_IN_A_FILE == 0:
                    file_cnt += 1
                    self.__write_split_file(file_cnt, first_col_names, contents_in_file)
                    contents_in_file = b''

            file_cnt += 1
            self.__write_split_file(file_cnt, first_col_names, contents_in_file)

