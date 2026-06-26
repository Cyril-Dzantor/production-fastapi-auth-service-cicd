from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str = "user"
    
    model_config = {"from_attributes": True}

class UserInDB(User):
    hashed_password: str
