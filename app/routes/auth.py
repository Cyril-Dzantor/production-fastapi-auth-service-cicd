from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.database import get_db
from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from app.models.user import User as UserModel
from app.models.token import RefreshToken, BlacklistedToken
from app.schemas.user import UserCreate, User
from app.schemas.token import Token, RefreshTokenRequest
from app.core.security import get_password_hash, create_access_token, create_refresh_token
from app.services.auth_service import authenticate_user
from app.core.deps import get_current_user, oauth2_scheme
from app.services.audit_service import log_event

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = UserModel(
        email=user_in.email,
        hashed_password=hashed_password,
        role="user"
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        log_event(db, "LOGIN_FAILED", details={"email": form_data.username})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    log_event(db, "LOGIN_SUCCESS", user_id=user.id)
    
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    # Store refresh token in database
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    # Verify token in DB
    db_token = db.query(RefreshToken).filter(RefreshToken.token == request.refresh_token).first()
    if not db_token or db_token.revoked or db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
    user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
    # Invalidate old token
    db_token.revoked = True
    db.commit()
    
    # Generate new tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    new_refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    # Store new refresh token
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    new_db_token = RefreshToken(
        token=new_refresh_token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(new_db_token)
    db.commit()
    
    log_event(db, "TOKEN_REFRESHED", user_id=user.id)
    
    return {
        "access_token": access_token, 
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    current_user: UserModel = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Log out the current user by blacklisting their access token.
    """
    # Blacklist the access token
    blacklisted_token = BlacklistedToken(token=token)
    db.add(blacklisted_token)
    db.commit()
    
    log_event(db, "LOGOUT_SUCCESS", user_id=current_user.id)
    
    return {"message": "Successfully logged out"}


