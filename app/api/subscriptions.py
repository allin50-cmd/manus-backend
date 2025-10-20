
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_subscription():
    return {"message": "Subscriptions endpoint"}
