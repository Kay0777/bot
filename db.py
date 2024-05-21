from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
import datetime

from config import CONF

DATABASE_URL = "postgresql+asyncpg://{}:{}@{}/{}".format(
    CONF['USER'], CONF['PASSWORD'], CONF['HOST'], CONF['DBNAME'],
)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="alive")
    status_updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


engine = create_async_engine(DATABASE_URL, echo=CONF['DEBUG'])
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
