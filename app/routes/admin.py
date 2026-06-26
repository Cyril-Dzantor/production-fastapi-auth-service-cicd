from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User as UserModel
from app.schemas.user import User
from app.core.database import get_db
from app.core.deps import RoleChecker

router = APIRouter(prefix="/admin", tags=["admin"])

# Create a dependency that requires the user to have the "admin" role
require_admin = RoleChecker(["admin"])

@router.get("/users", response_model=List[User])
def get_all_users(
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(require_admin)
):
    """
    Get a list of all users in the system.
    Requires the 'admin' role.
    """
    users = db.query(UserModel).all()
    return users
