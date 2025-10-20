
from fastapi import APIRouter

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session():
    return {"message": "Payment endpoint"}
