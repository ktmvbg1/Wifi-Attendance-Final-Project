from fastapi import APIRouter, Depends, Request, HTTPException, status
from services import device
from dtos.device import UpdateDeviceInput, CreateDeviceInput
from jose import JWTError
from dependencies import get_db, get_current_user, filter_request, teacher_endpoints
from sqlalchemy.orm import Session
from models import User


router = APIRouter(prefix="/api/devices",
                   tags=["devices"], dependencies=[Depends(filter_request)])


@router.get("/current-device")
async def get_current_devices(request: Request, r=Depends(filter_request)):
    return r


@router.get("/", dependencies=[Depends(teacher_endpoints)])
async def get_devices(session: Session = Depends(get_db)):
    data = device.get_devices(session)
    return data

@router.get("/{device_id}", dependencies=[Depends(teacher_endpoints)])
async def get_devices(device_id: int, session: Session = Depends(get_db)):
    data = device.get_device(session, device_id)
    return data


@router.post("/", dependencies=[Depends(teacher_endpoints)])
async def create_device(input: CreateDeviceInput, session: Session = Depends(get_db)):
    success, data = device.add_device(
        session, input.user_id, input.mac_address, input.ip_address)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=data,
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.patch("/{device_id}", dependencies=[Depends(teacher_endpoints)])
async def update_device(device_id: int, input: UpdateDeviceInput, session: Session = Depends(get_db)):
    success, data = device.update_device(
        session, device_id, input.user_id, input.mac_address, input.ip_address)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=data,
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.delete("/{device_id}", dependencies=[Depends(teacher_endpoints)])
async def delete_device(device_id: int, session: Session = Depends(get_db)):
    success, data = device.delete_device(
        session, device_id)
    if success:
        return {"success": True, "data": data}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=data,
        headers={"WWW-Authenticate": "Bearer"},
    )
