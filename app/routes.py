from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from datetime import timedelta
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__) ))

# Import database functions
from db import (
    init_db,
    get_user_by_id,
    get_all_users,
    create_user,
    get_device_by_id,
    get_devices_by_user_id,
    create_device,
    get_message_by_guid,
    get_messages_by_device_id,
    create_message,
    get_health_data_by_id,
    get_health_data_by_device_id,
    create_health_data
)

# Import authentication utilities
from app.auth import authenticate_user, get_current_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    # Initialize the database asynchronously when the app starts
    await init_db()

# Import SQLModel classes to reuse their structure
from app.models import Message, User, Device, HealthData

# Define all routes in a clean, non-circular structure

@app.get("/api")
async def read_root():
    return {"message": "Welcome to the Apple-Sync API"}

# Authentication endpoint
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint to authenticate user and return access token"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoints - require authentication
@app.get("/user/{user_id}")
async def get_user_protected(user_id: int, current_user: User = Depends(get_current_user)):
    try:
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/users")
async def get_users_protected(current_user: User = Depends(get_current_user)):
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/user")
async def create_user_endpoint_protected(user: User, current_user: User = Depends(get_current_user)):
    try:
        created_user = await create_user(user.user_name)
        return created_user
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Device endpoints (require authentication)
@app.get("/device/{device_id}")
async def get_device_protected(device_id: int, current_user: User = Depends(get_current_user)):
    try:
        device = await get_device_by_id(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/user/{user_id}/devices")
async def get_devices_for_user_protected(user_id: int, current_user: User = Depends(get_current_user)):
    try:
        # First check if the user exists
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        devices = await get_devices_by_user_id(user_id)
        return devices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/user/{user_id}/device")
async def create_device_for_user_protected(user_id: int, device: Device, current_user: User = Depends(get_current_user)):
    try:
        created_device = await create_device(device.device_name, user_id)
        return created_device
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Message endpoints (require authentication)
@app.get("/message/{guid}")
async def get_message_protected(guid: str, current_user: User = Depends(get_current_user)):
    try:
        message = await get_message_by_guid(guid)
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/device/{device_id}/messages")
async def get_messages_for_device_protected(device_id: int, current_user: User = Depends(get_current_user)):
    try:
        messages = await get_messages_by_device_id(device_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/device/{device_id}/message")
async def create_message_for_device_protected(device_id: int, message: Message, current_user: User = Depends(get_current_user)):
    try:
        created_message = await create_message(
            message.guid,
            message.conversation_guid,
            message.conversation_conversation,
            message.conversation_display_name,
            message.date,
            message.sender_full_name,
            message.sender_phone_numbers,
            message.type,
            message.body,
            device_id,
        )
        return created_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# HealthData endpoints (require authentication)
@app.get("/health/{health_id}")
async def get_health_data_protected(health_id: str, current_user: User = Depends(get_current_user)):
    try:
        health_data = await get_health_data_by_id(health_id)
        if health_data is None:
            raise HTTPException(status_code=404, detail="Health data not found")
        return health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/device/{device_id}/health")
async def get_health_data_for_device_protected(device_id: int, guid: Optional[str] = None, current_user: User = Depends(get_current_user)):
    try:
        # First check if the device exists
        device = await get_device_by_id(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        
        health_data = await get_health_data_by_device_id(device_id, guid)
        return health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/device/{device_id}/health")
async def create_health_data_for_device_protected(device_id: int, health_data: HealthData, current_user: User = Depends(get_current_user)):
    try:
        # First check if the device exists
        device = await get_device_by_id(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        
        created_health_data = await create_health_data(
            device_id,
            health_data.name,
            health_data.source,
            health_data.duration,
            health_data.startdate,
            health_data.enddate,
            health_data.unit,
            health_data.value,
            health_data.type
        )
        return created_health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")





# User endpoints
# @app.get("/user/{user_id}")
# async def get_user(user_id: int):
#     try:
#         user = await get_user_by_id(user_id)
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.get("/users")
# async def get_users():
#     try:
#         users = await get_all_users()
#         return users
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.post("/user")
# async def create_user_endpoint(user: User):
#     try:
#         created_user = await create_user(user.user_name)
#         return created_user
#     except Exception as e:
#         if "already exists" in str(e):
#             raise HTTPException(status_code=409, detail=str(e))
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# # Device endpoints
# @app.get("/device/{device_id}")
# async def get_device(device_id: int):
#     try:
#         device = await get_device_by_id(device_id)
#         if device is None:
#             raise HTTPException(status_code=404, detail="Device not found")
#         return device
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.get("/user/{user_id}/devices")
# async def get_devices_for_user(user_id: int):
#     try:
#         # First check if the user exists
#         user = await get_user_by_id(user_id)
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
        
#         devices = await get_devices_by_user_id(user_id)
#         return devices
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.post("/user/{user_id}/device")
# async def create_device_for_user(user_id: int, device: Device):
#     try:
#         created_device = await create_device(device.device_name, user_id)
#         return created_device
#     except Exception as e:
#         if "already exists" in str(e):
#             raise HTTPException(status_code=409, detail=str(e))
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# # Message endpoints
# @app.get("/message/{guid}")
# async def get_message(guid: str):
#     try:
#         message = await get_message_by_guid(guid)
#         if message is None:
#             raise HTTPException(status_code=404, detail="Message not found")
#         return message
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.get("/device/{device_id}/messages")
# async def get_messages_for_device(device_id: int):
#     try:
#         messages = await get_messages_by_device_id(device_id)
#         return messages
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.post("/device/{device_id}/message")
# async def create_message_for_device(device_id: int, message: Message):
#     try:
#         created_message = await create_message(
#             message.guid,
#             message.conversation_guid,
#             message.conversation_conversation,
#             message.conversation_display_name,
#             message.date,
#             message.sender_full_name,
#             message.sender_phone_numbers,
#             message.type,
#             message.body,
#             device_id,
#         )
#         return created_message
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# # HealthData endpoints
# @app.get("/health/{health_id}")
# async def get_health_data(health_id: str):
#     try:
#         health_data = await get_health_data_by_id(health_id)
#         if health_data is None:
#             raise HTTPException(status_code=404, detail="Health data not found")
#         return health_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.get("/device/{device_id}/health")
# async def get_health_data_for_device(device_id: int, guid: Optional[str] = None):
#     try:
#         # First check if the device exists
#         device = await get_device_by_id(device_id)
#         if device is None:
#             raise HTTPException(status_code=404, detail="Device not found")
        
#         health_data = await get_health_data_by_device_id(device_id, guid)
#         return health_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.post("/device/{device_id}/health")
# async def create_health_data_for_device(device_id: int, health_data: HealthData):
#     try:
#         # First check if the device exists
#         device = await get_device_by_id(device_id)
#         if device is None:
#             raise HTTPException(status_code=404, detail="Device not found")
        
#         created_health_data = await create_health_data(
#             device_id,
#             health_data.name,
#             health_data.source,
#             health_data.duration,
#             health_data.startdate,
#             health_data.enddate,
#             health_data.unit,
#             health_data.value,
#             health_data.type
#         )
#         return created_health_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
