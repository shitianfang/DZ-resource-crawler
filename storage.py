from sqlalchemy.orm import session
from sqlalchemy.sql.sqltypes import String, Unicode
from model import DBSession,Data,Mark
import json


def save_data(data,session):
    # {"title":title,"introduce":introduce,"value":value}
    # print(data)
    print("存储数据",data['value'])
    
    with session.no_autoflush:
        if not session.query(Data).filter(Data.id==data["id"]).first():
            # data["introduce"]=json.dumps(data["introduce"])
            session.add(Data(**data))
        
            session.commit()