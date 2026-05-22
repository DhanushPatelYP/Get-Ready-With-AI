from fastapi import APIRouter
from app.utils.response import success_response

router = APIRouter()

@router.get("/")
def health_check():
    return success_response(
        message="API is healthy"
    )