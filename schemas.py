from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    email: str
    
class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int