import json
import uuid


from fastapi import APIRouter, Depends, Path, HTTPException, requests, Request
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import url
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from auth.base_config import fastapi_users
from auth.models import User
from database import get_async_session, engine

from operations import models
from operations.models import operation, product, OperationCreate, ProductCreate, BasketCreate, basket, OrderCreate
from typing import ClassVar
from datetime import datetime

templates = Jinja2Templates(directory='templates')


# роутеры

main_router = APIRouter(
    prefix='',
    tags=['main'],
)


router_orders = APIRouter(
    prefix="/order",
    tags=["order"]
)



router3_basket = APIRouter(
    prefix="/basket",
    tags=["basket"]
)

router2 = APIRouter(
    prefix="",
    tags=["Product"]
)

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)
#################################


#Главная страница
@main_router.get('/')
async def main_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(models.product)
    result = await session.execute(query)
    x = [dict(r._mapping) for r in result]
    return templates.TemplateResponse('index.html', {"request": request, "x": x})





#################################
# Корзина
#################################

#### Удаление товаров из корзины
@router3_basket.post("/{user_id}/delete")
async def delete_basket(basket_delete: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(basket).where(basket.c.user_id == basket_delete)
    await session.execute(stmt)
    await session.commit()
    return RedirectResponse("index.html")



# добавление товара в корзину
@router3_basket.post("/{user_id}/add/{product_id}")
async def add_to_basket(bascet_create: BasketCreate, session: AsyncSession = Depends(get_async_session)):

    print(bascet_create)
    stmt = insert(basket).values(**bascet_create.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "create)"}







##########################################################################
#   Реализация поиска по категориям
##########################################################################

#Получить все товары
@router2.get("/get_product_all")
async def get_all_products(session: AsyncSession = Depends(get_async_session)):
    query = select(models.product)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]


@router2.get("/smartfons")
async def get_product(request: Request, session: AsyncSession = Depends(get_async_session)):
    xa = "смартфоны"
    query = select(models.product).where(product.c.type == xa)
    result = await session.execute(query)
    x = [dict(r._mapping) for r in result]
    return templates.TemplateResponse('index.html', {"request": request, "x": x})


@router2.get("/notebooks")
async def get_product(request: Request, session: AsyncSession = Depends(get_async_session)):
    xa = "ноутбуки"
    query = select(models.product).where(product.c.type == xa)
    result = await session.execute(query)
    x = [dict(r._mapping) for r in result]
    return templates.TemplateResponse('index.html', {"request": request, "x": x})


@router2.get("/PK")
async def get_product(request: Request, session: AsyncSession = Depends(get_async_session)):
    xa = "ПК"
    query = select(models.product).where(product.c.type == xa)
    result = await session.execute(query)
    x = [dict(r._mapping) for r in result]
    return templates.TemplateResponse('index.html', {"request": request, "x": x})


@router2.get("/accessories")
async def get_product(request: Request, session: AsyncSession = Depends(get_async_session)):
    xa = "Акксессуары"
    query = select(models.product).where(product.c.type == xa)
    result = await session.execute(query)
    x = [dict(r._mapping) for r in result]
    return templates.TemplateResponse('index.html', {"request": request, "x": x})








##########################################################################
#  SUPERUSER=TRUE  (для админа и достп только у админа)
##########################################################################


current_superuser = fastapi_users.current_user()

#Получить все товары  (без superuser)
@router2.get("/get_product_type")
async def get_product_type(product_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(models.product).where(product.c.type == product_type)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]

# поиск по имени товара (без superuser)
@router2.get("/get_product_name")
async def get_product_name(product_name: str, session: AsyncSession = Depends(get_async_session)):
    query = select(models.product).where(product.c.type == product_name)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]



# Создание товара
@router2.post("/product_create")
async def add_specific_products(product_create: ProductCreate, session: AsyncSession = Depends(get_async_session),
                                current_superuser: User = Depends(current_superuser)):
    if not current_superuser.is_superuser:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    stmt = insert(product).values(**product_create.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "create)"}




# Обновление товара
@router2.put("/product_update/{id}")
async def update_specific_products(product_update_id: int, updated_product: ProductCreate,
                                   session: AsyncSession = Depends(get_async_session),
                                   current_superuser: User = Depends(current_superuser)):
    if not current_superuser.is_superuser:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    query = update(product).where(product.c.id == product_update_id).values(**updated_product.dict(exclude_unset=True))
    result = await session.execute(query)
    await session.commit()
    return {"status": "upgrade_done"}


# обновление кол-ва товара
@router2.put("/product_availability_update/{id}")
async def update_specific_products(product_update_id: int, updated_availability: int,
                                   session: AsyncSession = Depends(get_async_session),
                                   current_superuser: User = Depends(current_superuser)):
    if not current_superuser.is_superuser:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    query = update(product).where(product.c.id == product_update_id).values(availability=updated_availability)
    result = await session.execute(query)
    await session.commit()
    return {"status": "availability_done"}




# Удаление товара
@router2.delete("/product_delete/{id}")
async def delete_specific_products(product_id: int, session: AsyncSession = Depends(get_async_session),
                                   current_superuser: User = Depends(current_superuser)
                                   ):
    if not current_superuser.is_superuser:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    stmt = delete(product).where(product.c.id == product_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "delete_done"}





##########################################################################
#  OPERATIONS - тренировочные функции
##########################################################################

@router.get("/get_type")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(models.operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]



@router.get("/get_all")
async def get_all_operations(session: AsyncSession = Depends(get_async_session)):
    query = select(models.operation)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]


# Создание опирации
@router.post("/operation_create")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


# Обновление
@router.put("/operation_update")
async def update_specific_operation(operation_id: int, updated_operation: OperationCreate,
                                    session: AsyncSession = Depends(get_async_session)):
    query = update(operation).where(operation.c.id == operation_id).values(**updated_operation.dict(exclude_unset=True))
    result = await session.execute(query)
    await session.commit()
    return {"status": "upgrade_done"}


# Удаление
@router.delete("/operation_delete/{id}")
async def delete_specific_operation(operation_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(operation).where(operation.c.id == operation_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
