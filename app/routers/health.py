from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def health_check() -> dict[str, str]:
    return {"message": "FastAPI is running!"}
