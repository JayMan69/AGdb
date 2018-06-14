from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import rds_config
from create_tables import Client,Camera
import json

class database:
    def __init__(self,id=None):
        Base = declarative_base()

        connection_string = "mysql://"+rds_config.db_username+':'+rds_config.db_password+ '@' +\
                            rds_config.db_endpoint+':'+ str(rds_config.db_port) +'/' + rds_config.db_name

        engine = create_engine(connection_string)
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        if id != None:
            self.id = id

    def get_clients(self):
        # List clients in the client table
        count = 0
        rs = []
        for instance in self.session.query(Client).order_by(Client.id):
            count = count + 1
            rs.append({instance.id:instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_client(self):
        # List clients in the client table
        count = 0
        rs = []
        for instance in self.session.query(Client).filter(Client.id== self.id):
            count = count + 1
            rs.append({instance.id:instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_cameras(self):
        # List clients in the client table
        count = 0
        rs = []
        for instance in self.session.query(Camera).order_by(Camera.id):
            count = count + 1
            rs.append({instance.id:instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_camera(self):
        # List clients in the client table
        count = 0
        rs = []
        for instance in self.session.query(Camera).filter(Camera.id== self.id):
            count = count + 1
            rs.append({instance.id:instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1



def testHarness():
    event = {}
    #event['camera_id'] = 10

    if 'camera_id' in event:
        db = database(event['camera_id'])
        body = db.get_camera()
    else:
        db = database()
        body = db.get_cameras()

    print(json.dumps(body))

if __name__ == '__main__':
    testHarness()