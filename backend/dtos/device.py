from ctypes import Union
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


class CreateDeviceInput(BaseModel):
    user_id: int
    mac_address: str
    ip_address: str

class UpdateDeviceInput(BaseModel):
    user_id: Optional[str]
    mac_address: Optional[str]
    ip_address: Optional[str]
