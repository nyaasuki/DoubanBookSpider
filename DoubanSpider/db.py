from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine('sqlite:///douban.db')
Base = declarative_base(engine)


class Douban(Base):
    __tablename__ = 'DouBan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String, unique=False, nullable=False)
    url = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<Douban(id='%d', tag='%s',url='%s')>" % (self.id, self.tag, self.url)

class Recording(Base):
    __tablename__ = 'Recording'
    id = Column(Integer, primary_key=True)
    data = Column(Integer, unique=True, nullable=False)

if os.path.isfile('douban.db') is False:
    print('正在创建数据库...')
    Base.metadata.create_all()
else:
    print('检测到现有数据库，正在读取...')

if __name__ == '__main__':
    # 重置数据库
    Base.metadata.drop_all(engine)
    print('Done')
