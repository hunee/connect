"""Illustrates the asyncio engine / connection interface.

In this example, we have an async engine created by
:func:`_engine.create_async_engine`.   We then use it using await
within a coroutine.

"""

#print('__FILE__: ', __file__)
import asyncio

import logging


import sqlalchemy as sa

from sqlalchemy.ext.asyncio import create_async_engine

#from ..config import config
from app.config import config, get_database_url


###
logger = logging.getLogger(__name__)

# engine is an instance of AsyncEngine
DATABASE_URL = get_database_url(config('mysql'))
logger.info('->> DATABASE_URL: ' + DATABASE_URL)

engine = create_async_engine(DATABASE_URL, connect_args={'auth_plugin': 'mysql_native_password'})#, echo=True)


###
meta = sa.MetaData()

question_sa = sa.Table(
        'question', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('question_text', sa.String(200), nullable=False),
        sa.Column('pub_date', sa.DateTime, server_default=sa.func.now()),

        # Indexes #
        sa.PrimaryKeyConstraint('id', name='question_id_pkey'),

        mysql_partitions="16",
        mysql_partition_by="LINEAR HASH(id)",

)


choice_sa = sa.Table(
        'choice', meta,
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('question_id', sa.Integer, nullable=False),
        sa.Column('choice_text', sa.String(200), nullable=False),
        sa.Column('votes', sa.Integer, server_default="0", nullable=False),

        # Indexes #
        sa.PrimaryKeyConstraint('id', name='choice_id_pkey'),
#        sa.ForeignKeyConstraint(['question_id'], [question_sa.c.id],
#                                name='choice_question_id_fkey',
#                                ondelete='CASCADE'),
)

t1 = sa.Table(
    "t1", meta, 
    sa.Column("id", sa.Integer, primary_key=True), 
    sa.Column("name", sa.String(200)),

    mysql_partitions="16",
    mysql_partition_by="LINEAR HASH(id)",

)

계정_정보 = sa.Table(
    '계정_정보', meta,
    sa.Column('id', sa.Integer, autoincrement=True, primary_key=True, comment='사용자_계정정보'),
    sa.Column('uuid', sa.String(255), nullable=False),
    sa.Column('사용자', sa.String(255), nullable=False),
    sa.Column('비밀번호', sa.String(255), nullable=False),
    sa.Column('마켓', sa.String(255), nullable=False, default=""),
    sa.Column('단말기', sa.String(255), nullable=False, default=""),
    sa.Column('운영체제', sa.String(255), nullable=False, default=""),
    sa.Column('운영체제_버전', sa.String(255), nullable=False, default=""),
    sa.Column('푸시_token', sa.String(255), nullable=False, default=""),
    sa.Column('비밀번호_찾기_재시도시간', sa.String(255), nullable=False, default=""),

    # Indexes #
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid', name='uniq_registry0uuid'),

    mysql_engine='InnoDB',
    mysql_collate='utf8mb4_unicode_ci',
    mysql_charset='utf8mb4',
    #mysql_partitions="16",
    #mysql_partition_by="LINEAR HASH(id)",
)    

계정_생성_정보 = sa.Table(
    '계정_생성_정보', meta,
    sa.Column('id', sa.Integer, autoincrement=True, primary_key=True, comment='사용자_계정정보'),
    sa.Column('날짜', sa.DateTime, server_default=sa.func.now()),
    sa.Column('마켓', sa.String(255), nullable=False),
    sa.Column('단말기', sa.String(255), nullable=False),
    sa.Column('운영체제', sa.String(255), nullable=False),
    sa.Column('운영체제_버전', sa.String(255), nullable=False),
    sa.Column('fk_계정_정보_id', sa.Integer),

    # Indexes #
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['fk_계정_정보_id'], ['계정_정보.id'], name='fk_계정_정보_id'),

    mysql_engine='InnoDB',
    mysql_collate='utf8mb4_unicode_ci',
    mysql_charset='utf8mb4',
    #mysql_partitions="16",
    #mysql_partition_by="LINEAR HASH(id)",
)    


async def connect():
    print('------------ connect')

    # conn is an instance of AsyncConnection
    async with engine.begin() as conn:

        # to support SQLAlchemy DDL methods as well as legacy functions, the
        # AsyncConnection.run_sync() awaitable method will pass a "sync"
        # version of the AsyncConnection object to any synchronous method,
        # where synchronous IO calls will be transparently translated for
        # await.
        
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

        # for normal statement execution, a traditional "await execute()"
        # pattern is used.
        
        result = await conn.execute(
            sa.insert(t1), [{"name": "13"}, {"name": "some name 2"}, {"name": "3"}, {"name": "33 some name 2"}, {"name": "15"}, {"name": "55some name 2"}]
        )
        print('result.rowcount: ' , result.rowcount)

        result = await conn.execute(
            question_sa.insert(), [{"question_text": "some name 1"}, {"question_text": "some name 2"}]
        )
        print('result.rowcount: ' , result.rowcount)
        

        result = await conn.execute(
            계정_정보.insert(), [{'uuid': 'uuid', '사용자': '1', '비밀번호':'비밀번호'}, {'uuid': 'uuid2', '사용자': '2', '비밀번호':'비밀번호'}]
        )
        print('result.rowcount: ' , result.rowcount)

    async with engine.connect() as conn:

        
        # the default result object is the
        # sqlalchemy.engine.Result object
        #result = await conn.execute(sa.text("SHOW DATABASES;"))
        stmt = (
            계정_정보.select().where(계정_정보.c.사용자 =='2')
        )
        #stmt = sa.text('SELECT * FROM 계정_정보 WHERE 사용자 = "2";')
        print('SQL: ' + str(stmt))

        result = await conn.execute(stmt)

        # the results are buffered so no await call is necessary
        # for this case.
        row = result.first()
        print('result.rowcount: ' + str(result.rowcount))
        print('사용자: ' + row.사용자)
        print('비밀번호: ' + row.비밀번호)
        print("list of rows: %s" % row)

        #a1.비밀번호 = "new data"
        stmt = (
                t1.update().
                where(t1.c.id == '2').
                values(name='user #5')
            )

        result = await conn.execute(stmt)
        print('result.rowcount: ' , result.rowcount)
        

        await conn.commit()

        # for a streaming result that buffers only segments of the
        # result at time, the AsyncConnection.stream() method is used.
        # this returns a sqlalchemy.ext.asyncio.AsyncResult object.
        async_result = await conn.stream(t1.select())

        #async for partition in async_result.partitions(1):
        #    print("list of rows: %s" % partition)

        # this object supports async iteration and awaitable
        # versions of methods like .all(), fetchmany(), etc.
        #async for row in async_result:
            #print("name:", row['name'], "; id: ", row['id'])

        row = await async_result.first()
        print("list of rows: %s" % row)

        #async for id, name in async_result:
        #    print("id:", id, "; name: ", name)            