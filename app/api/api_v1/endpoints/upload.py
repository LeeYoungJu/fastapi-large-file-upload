import os

import boto3
from fastapi import APIRouter, HTTPException, Request, status
from starlette.requests import ClientDisconnect
import uuid

from app.consts import Path

router = APIRouter()


@router.post('/')
async def upload(request: Request):
    # body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)
    filename = request.headers.get('Filename')

    if not filename:
        raise (HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                             detail='Filename header is missing'))
    try:
        # filepath = os.path.join('./', os.path.basename(filename))
        # file_ = FileTarget(filepath, validator=MaxSizeValidator(MAX_FILE_SIZE))
        # data = ValueTarget()
        # parser.register('file', file_)
        # parser.register('data', data)
        count = 0
        counter = 1
        tmp_path = os.path.join(Path.APP_DIR, 'tmp')
        file_name = uuid.uuid4()
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)
        file_path = os.path.join(tmp_path, f"{file_name}{counter}.csv")

        f = open(file_path, 'wb+')
        async for chunk in request.stream():
            print(chunk)
            count += chunk.count(b'\n')
            print(count)
            if count > 2:
                required_new_lines = 2 - count
                print(required_new_lines)
                new_lines = chunk.split(b'\n')[:required_new_lines]
                print(new_lines)
                chunk = b'\n'.join(chunk.split(b'\n')[required_new_lines:])
                count = 0
                f.write(b'\n'.join(new_lines))
                s3 = boto3.client('s3',
                                  endpoint_url="http://127.0.0.1:9000/",
                                  aws_access_key_id='minioadmin',
                                  aws_secret_access_key='minioadmin')
                s3.upload_file(file_path, 'yjlee', f"{file_name}{counter}.csv")
                counter += 1
                f.close()
                f = open(file_path, 'wb+')
            f.write(chunk)
            # if chunks.count(b"\n") >= 10000:
            #     a = chunks.split(b"\n")[:10000]
            #     b''.join(a)
            #     chunks =  b''.join(chunks.split(b"\n")[10000:])
            #     print("hello")
            # body_validator(chunk)

    except ClientDisconnect:
        print("Client Disconnected")
    # except MaxBodySizeException as e:
    #     raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    #        detail=f'Maximum request body size limit ({MAX_REQUEST_BODY_SIZE} bytes) exceeded ({e.body_len} bytes read)')
    # except streaming_form_data.validators.ValidationError:
    #     raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    #         detail=f'Maximum file size limit ({MAX_FILE_SIZE} bytes) exceeded')

    # if not file_.multipart_filename:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='File is missing')

    # print(data.value.decode())
    # print(file_.multipart_filename)

    return {"message": f"Successfuly uploaded {filename}"}