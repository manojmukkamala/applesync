#!/usr/bin/env python3
import os
import sys
from typing import Any

from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware

from .security import get_api_key

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__) ))

# Import database functions
from db import (
    create_device,
    create_health_data,
    create_message,
    create_screen_time,
    create_user,
    get_all_users,
    get_device_by_id,
    get_devices_by_user_id,
    get_health_data_by_device_id,
    get_health_data_by_id,
    get_message_by_guid,
    get_messages_by_device_id,
    get_screen_time_by_device_id,
    get_screen_time_by_id,
    get_user_by_id,
    init_db,
)

# Import SQLModel classes to reuse their structure
from app.models import Device, HealthData, Message, ScreenTime, User

app = FastAPI(
    title="Applesync API",
    description="API for iOS data synchronization",
    version="4.0.0",
    dependencies=[Security(get_api_key)],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.on_event("startup")
async def on_startup() -> None:
    # Initialize the database asynchronously when the app starts
    await init_db()

# Define all routes in a clean, non-circular structure

@app.get("/api")
async def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Apple-Sync API"}

# User endpoints
@app.get("/user/{user_id}")
async def get_user(user_id: int) -> dict[str, Any] | None:
    try:
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}") from e

@app.get("/users")
async def get_users() -> list[dict[str, Any]]:
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}") from e

@app.post("/user")
async def create_user_endpoint(user: User) -> dict[str, Any]:
    try:
        created_user = await create_user(user.user_name)
        return created_user
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e)) from e
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}") from e

# Device endpoints
@app.get("/device/{device_id}")
async def get_device(device_id: int) -> dict[str, Any] | None:
    try:
        device = await get_device_by_id(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.get("/user/{user_id}/devices")
async def get_devices_for_user(user_id: int) -> list[dict[str, Any]]:
    try:
        # First check if the user exists
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        devices = await get_devices_by_user_id(user_id)
        return devices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.post("/user/{user_id}/device")
async def create_device_for_user(user_id: int, device: Device) -> dict[str, Any]:
    try:
        created_device = await create_device(device.device_name, user_id)
        return created_device
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

# Message endpoints
@app.get("/message/{guid}")
async def get_message(guid: str) -> dict[str, Any] | None:
    try:
        message = await get_message_by_guid(guid)
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.get("/device/{device_id}/messages")
async def get_messages_for_device(device_id: int, guid: str | None = None, start_date: str | None = None, end_date: str | None = None) -> list[dict[str, Any]] | None:
    try:
        messages = await get_messages_by_device_id(device_id, guid, start_date, end_date)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.post("/device/{device_id}/message")
async def create_message_for_device(device_id: int, message: Message) -> dict[str, Any]:
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
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

# HealthData endpoints
@app.get("/health/{health_id}")
async def get_health_data(health_id: str) -> dict[str, Any] | None:
    try:
        health_data = await get_health_data_by_id(health_id)
        if health_data is None:
            raise HTTPException(status_code=404, detail="Health data not found")
        return health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.get("/device/{device_id}/health")
async def get_health_data_for_device(device_id: int, guid: str | None = None, start_date: str | None = None, end_date: str | None = None) -> list[dict[str, Any]] | None:
    try:
        # First check if the device exists
        device = await get_device_by_id(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        health_data = await get_health_data_by_device_id(device_id, guid, start_date, end_date)
        return health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.post("/device/{device_id}/health")
async def create_health_data_for_device(device_id: int, health_data: HealthData) -> dict[str, Any]:
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
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

# ScreenTime endpoints
@app.get("/screen-time/{screen_time_id}")
async def get_screen_time(screen_time_id: str) -> dict[str, Any] | None:
    try:
        screen_time = await get_screen_time_by_id(screen_time_id)
        if screen_time is None:
            raise HTTPException(status_code=404, detail="Screen time not found")
        return screen_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.get("/device/{device_id}/screen-time")
async def get_screen_time_for_device(device_id: int, app: str | None = None, start_date: str | None = None, end_date: str | None = None) -> list[dict[str, Any]]:
    try:
        # First check if the device exists
        device = await get_device_by_id(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        screen_time = await get_screen_time_by_device_id(device_id, app, start_date, end_date)
        return screen_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")

@app.post("/device/{device_id}/screen-time")
async def create_screen_time_for_device(device_id: int, screen_time: ScreenTime) -> dict[str, Any]:
    try:
        # First check if the device exists
        device = await get_device_by_id(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        created_screen_time = await create_screen_time(
            device_id,
            screen_time.app,
            screen_time.website,
            screen_time.duration,
            screen_time.description,
            screen_time.activity_date
        )
        return created_screen_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e!s}")
