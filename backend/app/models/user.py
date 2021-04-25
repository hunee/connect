#print('__FILE__: ', __file__)

import asyncio
import logging
import typing

import sqlalchemy as sa

from sqlalchemy import bindparam
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker


#from ..config import config
import connect

from app.config import config, get_database_url


###
logger = logging.getLogger(__name__)

# engine is an instance of AsyncEngine
DATABASE_URL = get_database_url(config('mysql'))
logger.info('->> DATABASE_URL: ' + DATABASE_URL)

engine = create_async_engine(DATABASE_URL, connect_args={'auth_plugin': 'mysql_native_password'})#, echo=True)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


Base = declarative_base()

'''
class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String(200))
    create_date = Column(DateTime, server_default=func.now())
    bs = relationship("B")

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id = Column(ForeignKey("a.id"))
    data = Column(String(200))

class ACOUNT(Base):
    __tablename__ = "acount"
    __table_args__ = (
        #{'mysql_collate': 'utf8_general_ci'},
        {
            'mysql_engine':'InnoDB',
            'mysql_collate':'utf8mb4_unicode_ci',
            'mysql_charset':'utf8mb4',
            'mysql_partitions':'16',
            'mysql_partition_by':'LINEAR HASH(id)'
        }
    )

    id = Column(Integer, primary_key=True)
    user = Column(String(20))
    password = Column(String(20), index=True)
    create_date = Column(DateTime, server_default=func.now())
    #user_id = Column(ForeignKey("a.id"))
    bid = Column(String(20))
    foo = Column(String(20))
    user_index = Column(String(20), index=True)
    user_index2 = Column(String(20), index=True)
    운영체제_버전 = Column(String(255), nullable=True)
'''
class ACCOUNT(Base):
    __tablename__ = "계정_생성_정보"

    id = Column(Integer, primary_key=True)
    날짜 = Column(DateTime, server_default=func.now())
    마켓 = Column(String(20))
    단말기 = Column(String(20))

    운영체제 = Column(String(255), nullable=False, default="")
    운영체제_버전 = Column(String(255), nullable=False, default="")

    fk_계정_정보_id = Column(Integer)#, ForeignKey("계정_정보.id"))

    #bs = relationship("계정_정보")

@connect.profile
async def connect_begin():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        #await conn.run_sync(Base.metadata.create_all)
        pass


@connect.profile
async def add_user():

    async with async_session() as session:
        async with session.begin():
            session.add(
                ACCOUNT(단말기="bbb", 마켓="b")            
            )

            session.add_all(
            [
                ACCOUNT(단말기="a1", 마켓="b"),
                ACCOUNT(단말기="a2", 마켓="b"),
                ACCOUNT(단말기="a3", 마켓="b"),
                ACCOUNT(단말기="a4", 마켓="b"),
                ACCOUNT(단말기="a5", 마켓="b") ,                                                               
            ]
            )

            # for relationship loading, eager loading should be applied.
            stmt = select(ACCOUNT).order_by(ACCOUNT.fk_계정_정보_id)

            # for streaming ORM results, AsyncSession.stream() may be used.
            result = await session.execute(stmt)
            
            
            # result is a streaming AsyncResult object.
            for a1 in result.scalars():
                #print(a1)
                pass
                print(f"id: {a1.id}")
                print(f"fk_계정_정보_id: {a1.fk_계정_정보_id}")
                print(f"단말기: {a1.단말기}")
                print(f"마켓: {a1.마켓}")
            

            name = 'a2'
            stmt = select(ACCOUNT).where(ACCOUNT.단말기 == name)
            result = await session.stream(stmt)

            a2 = await result.scalars().first()
            if a2 is not None:
                #print(a2)
                pass
                print(f"단말기: {a2.단말기}")
                #print(f"password: {a2.password}")
                #print(f"created at: {a2.create_date}")

                a2.마켓 = '5'
                #await session.commit()


            # for relationship loading, eager loading should be applied.
            stmt = select(ACCOUNT).order_by(ACCOUNT.id)

            # for streaming ORM results, AsyncSession.stream() may be used.
            result = await session.stream(stmt)
            if result is not None:

                # result is a streaming AsyncResult object.
                async for a1 in result.scalars():
                    #print(a1)
                    print(f"user: {a1.단말기}")
                    #print(f"password: {a1.password}")
                    #print(f"created at: {a1.create_date}")

'''
async def add_user():
  async with engine.begin() as conn:
    #await conn.run_sync(Base.metadata.drop_all)
    #await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
      async with session.begin():
        session.add_all(
        [
            A(bs=[B(), B()], data="a1"),
            A(bs=[B()], data="a2"),
            A(bs=[B(), B()], data="a3"),
            ACOUNT(user="a", password="b")
        ]
        )

      # for relationship loading, eager loading should be applied.
      stmt = select(A).options(selectinload(A.bs))

      # AsyncSession.execute() is used for 2.0 style ORM execution
      # (same as the synchronous API).
      result = await session.execute(stmt)

      # result is a buffered Result object.
      for a1 in result.scalars():
          print(a1)
          print(f"created at: {a1.create_date}")
          for b1 in a1.bs:
              print(b1)

      # for streaming ORM results, AsyncSession.stream() may be used.
      result = await session.stream(stmt)

      # result is a streaming AsyncResult object.
      async for a1 in result.scalars():
          print(a1)
          for b1 in a1.bs:
              print(b1)

      result = await session.execute(select(A).order_by(A.id))

      a1 = result.scalars().first()

      a1.data = "new data"

      await session.commit()
    
'''    