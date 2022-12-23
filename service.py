from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from models import *


# Функции для работы с данными в БД
async def get_stores(session: AsyncSession) -> list[Store]:
    result = await session.execute(select(Store))
    return result.scalars().all()


async def get_items(session: AsyncSession) -> list[Item]:
    result = await session.execute(select(Item))
    return result.scalars().all()


async def get_sales(session: AsyncSession) -> list[Sales]:
    result = await session.execute(select(Sales))
    return result.scalars().all()


async def get_top_items(session: AsyncSession) -> list[Sales]:
    result = await session.execute(
        select(Sales.item_id, func.count(Sales.item_id), Item.name).join(Item, Item.id == Sales.item_id).group_by(Sales.item_id, Item.name).order_by(desc(func.count(Sales.item_id))).limit(10))
    return result.all()


async def get_top_stores(session: AsyncSession) -> list[Sales]:
    result = await session.execute(
        select(Sales.store_id, Store.address, func.sum(Item.price)).join(Store, Store.id == Sales.store_id).join(Item, Item.id == Sales.item_id).group_by(Sales.store_id, Store.address).order_by(desc(func.sum(Item.price))).limit(10))
    return result.all()


def add_sale(session: AsyncSession, item_id: int, store_id: int):
    new_sale = Sales(item_id=item_id, store_id=store_id)
    session.add(new_sale)
    return new_sale
