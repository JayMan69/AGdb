import pkg_resources
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from AGdb.rds_config import db_username,db_password,db_endpoint,db_port,db_name
from AGdb.create_tables import Client,Camera,Client_Cameras,Stream,Stream_Details,Stream_MetaData,\
    Stream_Details_Raw,Stream_Details_TS,Analytics_MetaData
import json
import datetime
from sqlalchemy.dialects import mssql
from sqlalchemy import func

class database:
    def __init__(self,id=None):
        Base = declarative_base()

        connection_string = "mysql://"+db_username+':'+db_password+ '@' +\
                            db_endpoint+':'+ str(db_port) +'/' + db_name

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
            rs.append({'id':instance.id,'name':instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_client(self):
        # List clients in the client table
        count = 0
        rs = []
        for instance in self.session.query(Client).filter(Client.id== self.id):
            count = count + 1
            rs.append({'id':instance.id,'name':instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_cameras(self):
        # List clients in the client table
        count = 0
        rs = []
        for instance in self.session.query(Camera).order_by(Camera.id):
            count = count + 1
            rs.append({'id':instance.id,'name':instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_camera(self):
        # List cameras in the camera table
        count = 0
        rs = []
        for instance in self.session.query(Camera).filter(Camera.id== self.id):
            count = count + 1
            rs.append({'id':instance.id,'name':instance.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_client_camera(self):
        # List clients in the client_camera table
        count = 0
        rs = []

        for instance in self.session.query(Client,Camera,Client_Cameras).filter(Client.id== self.id) \
                .filter(Client.id == Client_Cameras.client_id):
            count = count + 1
            rs.append({'id':instance.Camera.id,'name':instance.Camera.name})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_stream(self):
        # List streams given camera id
        count = 0
        rs = []
        for instance in self.session.query(Stream).filter(Camera.id== self.id):
            count = count + 1
            rs.append({'id':instance.id,'name':instance.stream_name,'arn':instance.arn,'region':instance.region})
        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_stream_object(self,query_column,value):
        # get stream object with camera id given stream name
        if query_column == 'arn':
            instance = self.session.query(Stream).filter(Stream.arn== value).first()

        return instance

    def get_stream_details(self):
        # List streams given camera id
        count = 0
        rs = []
        for instance in self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id) \
                .filter(Camera.id == Stream.camera_id, Stream.id == Stream_Details.stream_id):
            count = count + 1
            rs.append({'name':instance.Stream.stream_name,
                       'arn': instance.Stream.arn,
                       'id':instance.Stream_Details.id,
                       'manifest_file_name':instance.Stream_Details.manifest_file_name,
                       'live':instance.Stream_Details.live,
                       'start_time':instance.Stream_Details.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'end_time':instance.Stream_Details.end_time.strftime('%Y-%m-%d %H:%M:%S')})

        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_stream_details_object(self,query_column,p_object):
        # if start time is found, we need to delete everything in attendant tables and rerun
        if query_column == 'start_time':
            instance = self.session.query(Stream_Details).filter(Stream_Details.stream_id== p_object.stream_id)\
                                                         .filter(Stream_Details.start_time == p_object.start_time).first()

        return instance

    def get_stream_details_by_time(self,stime,etime):
        # List streams given camera id and time parameters
        count = 0
        rs = []
        stime = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
        etime = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        #q = self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id)\
        #        .filter(Camera.id == Stream.camera_id , Stream.id == Stream_Details.stream_id) \
        #        .filter(Stream_Details.start_time >= stime, Stream_Details.end_time <= etime)
        #q1 = str(q.statement.compile(dialect=mssql.dialect()))

        for instance in self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id)\
                .filter(Camera.id == Stream.camera_id , Stream.id == Stream_Details.stream_id) \
                .filter(Stream_Details.start_time >= stime, Stream_Details.end_time <= etime) :
            count = count + 1
            rs.append({'name':instance.Stream.stream_name,
                       'arn': instance.Stream.arn,
                       'id':instance.Stream_Details.id,
                       'manifest_file_name':instance.Stream_Details.manifest_file_name,
                       'live':instance.Stream_Details.live,
                       'start_time':instance.Stream_Details.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'end_time':instance.Stream_Details.end_time.strftime('%Y-%m-%d %H:%M:%S')})

        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_stream_metadata_by_time(self,stime,etime,label):
        # List streams given camera id and time parameters
        # TODO need to send back non contigous labels only
        count = 0
        rs = []
        stime = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
        etime = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        #q = self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id)\
        #        .filter(Camera.id == Stream.camera_id , Stream.id == Stream_Details.stream_id) \
        #        .filter(Stream_Details.start_time >= stime, Stream_Details.end_time <= etime)
        #q1 = str(q.statement.compile(dialect=mssql.dialect()))
        label = label.split(',')
        for instance in self.session.query(Stream,Stream_Details,Stream_MetaData ).filter(Stream.camera_id== self.id)\
                .filter(Stream.id == Stream_Details.stream_id , Stream_Details.id == Stream_MetaData.stream_details_id) \
                .filter(Stream_Details.start_time >= stime, Stream_Details.end_time <= etime) \
                .filter(Stream_MetaData.label.in_(label)):
            count = count + 1
            rs.append({'name':instance.Stream.stream_name,
                       'arn': instance.Stream.arn,
                       'id':instance.Stream_Details.id,
                       'label':instance.Stream_MetaData.label,
                       'manifest_file_name':instance.Stream_Details.manifest_file_name,
                       'live':instance.Stream_Details.live,
                       'label_timestamp':instance.Stream_MetaData.timestamp,
                       'start_time':instance.Stream_Details.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'end_time':instance.Stream_Details.end_time.strftime('%Y-%m-%d %H:%M:%S')})

        rs1 = {'count':count,'result_set':rs}
        return rs1


    def get_stream_metadata_by_time1(self,stime,etime,label):
        # List stream meta data given camera id and time parameters
        count = 0
        rs = []
        query_as_string = "select Stream.stream_name,Stream.arn,Stream_Details.id,label,Stream_Details.manifest_file_name, " \
                          "Stream_Details.live, Stream_Details.start_time,Stream_Details.end_time " \
                          "from Stream,Stream_Details,Stream_MetaData " \
                          "where Stream.id = Stream_Details.stream_id and Stream_Details.id = Stream_MetaData.stream_details_id " \
                          "AND " + "Stream.camera_id= " + str(self.id) + " and " + "Stream_Details.start_time >= '" + stime + "' "\
                          "AND Stream_Details.end_time <= '" + etime + "'" + " AND Stream_MetaData.label in(" + self.quote(label) + ")"

        # Run as query as in statement does not work!
        result = self.session.execute(query_as_string)
        for (stream_name,arn,id,label,manifest_file_name,live,start_time,end_time) in result:
            count = count + 1
            rs.append({'name':stream_name,
                       'arn': arn,
                       'id':id,
                       'label':label,
                       'manifest_file_name':manifest_file_name,
                       'live':live,
                       'start_time':start_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'end_time':end_time.strftime('%Y-%m-%d %H:%M:%S')})

        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_analytics_metaData_object(self,key):
        instance = self.session.query(Analytics_MetaData).filter(Analytics_MetaData.key == key).first()
        return instance


    def quote(self,label):
        x = ""
        count = 0
        label = label.split(',')
        for i in label:
            x = x + "'" + i + "'"
            count = count  + 1
            if count < len(label):
                x = x + ","
        return x

    def put_stream_details(self,p_object):
        # TODO package this https://python-packaging.readthedocs.io/en/latest/
        # https://www.pythonsheets.com/notes/python-sqlalchemy.html
        row = Stream_Details(stream_id=p_object.stream_id,
                             manifest_file_name=p_object.manifest_file_name,
                             live = p_object.live,
                             start_time = p_object.start_time,
                             end_time = p_object.end_time)
        self.session.add(row)
        return

    def put_stream_details_raw(self,p_object):
        row = Stream_Details_Raw(stream_details_id=p_object.stream_details_id,
                                 rawfilename=p_object.rawfilename,
                                 server_time = p_object.server_time)
        self.session.add(row)

        return

    def put_stream_details_ts(self,p_object):
        row = Stream_Details_TS(stream_details_id=p_object.stream_details_id,
                                transportname=p_object.transportname,
                                 server_time = p_object.server_time)
        self.session.add(row)

        return


    def put_stream_metadata(self,p_object):
        row = Stream_MetaData(stream_details_id=p_object.stream_details_id,
                                transportname=p_object.transportname,
                                 server_time = p_object.server_time)
        self.session.add(row)

        return

    def update_stream(self,p_object):
        stmt = update(Stream_Details).where(Stream_Details.id == p_object.id). \
            values(live='False')

    def update_analytics_metaData(self,p_object):
        newval = int(p_object.value) + 1
        p_object.value = str(newval)
        self.session.commit()

def testHarness():
    event = {}
    event['camera_id'] = 1
    event['label'] = 'person,duck'

    # db = database('1')
    # instance = db.get_analytics_metaData_object('raw_file_next_value')
    # db.update_analytics_metaData(instance)

    db = database('2')
    p_object = Stream_Details
    p_object.stream_id = 2
    p_object.start_time = datetime.datetime.strptime('2018-06-1 9:02:02', '%Y-%m-%d %H:%M:%S')
    instance = db.get_stream_details_object('start_time',p_object)
    print('')

    if 'client_id' in event:
        db = database(event['client_id'])
        body = db.get_client_camera()
        #print(json.dumps(body))

    if 'camera_id' in event:
        db = database(event['camera_id'])
        body = db.get_stream_details()
        #print(json.dumps(body))
        s = '2018-05-01 11:00:00'
        e = '2018-06-15 09:02:02'
        label = event['label']
        body = db.get_stream_metadata_by_time(s,e,label)
        print(json.dumps(body))

if __name__ == '__main__':
    testHarness()