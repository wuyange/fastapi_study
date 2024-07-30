from fastapi import Depends, APIRouter

doctor_info = APIRouter(prefix="/doctor_info")

@doctor_info.get("/test")
async def test():
    return {"message": "test"}