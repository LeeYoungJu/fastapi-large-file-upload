from pydantic import BaseModel


class ResponseData(BaseModel):
    status: bool
    data: dict

    @staticmethod
    def ok(data):
        return {
            'status': True,
            'data': data,
        }
