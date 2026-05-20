from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {
        "status":"success",
        "message":"API is Healthy"
    }