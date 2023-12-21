from typing import Optional

from fastapi_users import schemas



# чтение user(то что приходит после создания юзера)
class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    number: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True



# создание user(выборка того, что нужно для регистрации)
class UserCreate(schemas.BaseUserCreate):
    username: str
    number: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
