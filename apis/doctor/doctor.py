from fastapi import Depends, APIRouter

doctor = APIRouter(prefix="/doctor")

@doctor.get("/test")
async def test():
    return {"message": "test"}