from .doctor import doctor
from .hospital import hospital
from .payorders import payorders
from .useroders import userorders
from fastapi import FastAPI


def init_router(app: FastAPI) -> None:
    app.include_router(doctor)
    app.include_router(hospital)
    app.include_router(payorders)
    app.include_router(userorders)