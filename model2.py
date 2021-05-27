# 导入:
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Data(Base):
    # 表的名字:
    __tablename__ = 'data'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    title = Column(String)
    introduce=Column(String)
    value=Column(String)


class Mark(Base):
    
    __tablename__='mark'

    id=Column(Integer,primary_key=True)

# 初始化数据库连接:

basedir=os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'datas.db?check_same_thread=False')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


if __name__=="__main__":
    print("重建数据库")
    Base.metadata.create_all(engine)