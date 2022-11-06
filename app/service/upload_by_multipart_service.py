import os

import uuid
from fastapi import UploadFile

from app.consts import PATH


class UploadByMultipartService:

    def __init__(self):
        uuid_val = str(uuid.uuid4())
        self.tmp_path = os.path.join(PATH.APP_DIR, 'tmp', uuid_val)
        if not os.path.isdir(self.tmp_path):
            os.makedirs(self.tmp_path)

    async def upload(self, file: UploadFile):
        contents = await file.read()
        file_path = os.path.join(self.tmp_path, file.filename)
        with open(file_path, "wb") as fp:
            fp.write(contents)

        return self.tmp_path
