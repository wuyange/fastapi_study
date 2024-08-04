from pydantic import BaseModel
from fastapi import Query


class WxCodeForm(BaseModel):
    code: str = Query(..., description='微信code')