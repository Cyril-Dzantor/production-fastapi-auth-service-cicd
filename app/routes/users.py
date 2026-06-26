from fastapi import APIRouter, Depends
from app.models.user import User as UserModel
from app.schemas.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile", response_model=User)
def get_profile(current_user: UserModel = Depends(get_current_user)):
    """
    Get the current logged-in user's profile.
    Requires a valid JWT token.
    """
    return current_user
