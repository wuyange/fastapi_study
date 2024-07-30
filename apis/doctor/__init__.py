from fastapi import APIRouter
from .doctor import doctor_info


doctor = APIRouter(prefix="/api/v1/doctor")
doctor.include_router(doctor_info)