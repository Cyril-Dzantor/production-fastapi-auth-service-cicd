from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password
from typing import Optional

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Check if a user exists and the password is correct.
    Returns the user object if valid, None otherwise.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
