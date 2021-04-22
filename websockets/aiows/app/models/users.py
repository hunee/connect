import sqlalchemy as sa

meta = sa.MetaData()

사용자_정보 = sa.Table('사용자_정보', meta,
                  sa.Column('사용자_id', sa.Integer, nullable=False),
                  sa.Column('비밀번호', sa.String(200), nullable=False),
                  sa.Column('등록_날짜', sa.Date, nullable=False),
                  sa.PrimaryKeyConstraint('사용자_id', name='사용자_id_pkey'))

