from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Docstring for health_check
    """
    return {"status": "ok"}