from fastapi import FastAPI, Depends
from auth.base_config import auth_backend, fastapi_users
from auth.models import User
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_operation
from operations.router import router2 as router_product
from operations.router import router3_basket as router_basket
from operations.router import main_router
from fastapi.staticfiles import StaticFiles



app = FastAPI(
    title="ЭлектроМания"
)

# подключение статики
app.mount("/static", StaticFiles(directory="static"), name="static")


# роутеры авторизации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
#########

# импортирование роутеров из router.py
app.include_router(router_operation)
app.include_router(router_product)
app.include_router(router_basket)
app.include_router(main_router)
##################



#####################################
# различные проверки для пользователя в docs
#####################################
# проверяет человека по cookie и просто здоровается
current_user = fastapi_users.current_user()
@app.get("/just_reg-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"

# проверяет человека по cookie и на то что его аккаунт активен и просто здоровается
current_active_user = fastapi_users.current_user(active=True)
@app.get("/active_and_reg-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"

# проверяет человека по cookie и на то что его аккаунт верифицирован и просто здоровается
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
@app.get("/active_verifaed-route")
def protected_route(user: User = Depends(current_active_verified_user)):
    return f"Hello, {user.email}"

# проверяет человека по cookie и на то что его аккаунт суперпользователя и просто здоровается
current_superuser = fastapi_users.current_user(active=True, superuser=True)
@app.get("/active_superuser-route")
def protected_route(user: User = Depends(current_superuser)):
    return f"Hello, {user.email}"

#####################################