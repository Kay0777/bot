from sqlalchemy.future import select
from db import async_session, User
from typing import Union
import datetime


async def getAliveUsers() -> list[User]:
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(select(User).where(User.status == 'alive'))
            users = users.scalars().all()
            return users


async def updateUserStatusByID(user_id: int, status: str) -> bool:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()

            user.status = status
            user.status_updated_at = datetime.datetime.utcnow()
            await session.commit()
            return True


async def getUserByID(id: int) -> Union[User, None]:
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, id)
            return user


async def createUserByID(id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            user = User(id=id)
            session.add(user)
            await session.commit()
