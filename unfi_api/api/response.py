from typing import Any, Optional
from pydantic import BaseModel, validator
from requests import Response

"""        "error": error,
        "status": status,
        "data": data,
        "content_type": response.content,
        "text": response.text,
        "response": response"""


class APIResponse(BaseModel):
    status: int
    data: Optional[dict]
    error: Optional[str]
    text: Optional[str]
    # reason:  str
    content: Optional[bytes]
    response: Response

    class Config:
        arbitrary_types_allowed = True

    @validator('response', allow_reuse=True)
    def response_validator(cls, v):
        if not isinstance(v, Response):
            raise ValueError('Response must be a requests.Response object')
        return v
    
    @validator('status', allow_reuse=True)
    def http_status_validator(cls, v):
        if not isinstance(v, int):
            raise ValueError('Status must be an integer')
        if v < 200 or v > 599:
            raise ValueError('Status must be between 200 and 599')
        return v


class NonJsonResultError(Exception):
    super().__init__(Exception)