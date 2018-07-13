import pkg_resources
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from AGdb.rds_config import db_username,db_password,db_endpoint,db_port,db_name
#from .rds_config import db_username,db_password,db_endpoint,db_port,db_name
from AGdb.create_tables import Client,Camera,Client_Cameras,Stream,Stream_Details,Stream_MetaData,\
    Stream_Details_Raw,Stream_Details_TS,Analytics_MetaData
import json
import datetime
from sqlalchemy.dialects import mysql
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce

class Object(object):
    pass


class database:
    def __init__(self,id=None):
        Base = declarative_base()

        connection_string = "mysql://"+db_username+':'+db_password+ '@' +\
                            db_endpoint+':'+ str(db_port) +'/' + db_name

        engine = create_engine(connection_string)
        Base.metadata.bind = engine
        self.engine = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        if id != None:
            self.id = id

    def close(self):
        self.session.close()
        self.engine.dispose()

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
                .filter(Client.id == Client_Cameras.client_id) \
                .filter(Camera.id == Client_Cameras.camera_id):
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

    def get_stream_details(self,live='False'):
        # List streams given camera id
        count = 0
        rs = []
        if live == 'False':
            for instance in self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id) \
                    .filter(Camera.id == Stream.camera_id, Stream.id == Stream_Details.stream_id):
                count = count + 1
                rs.append({'name':instance.Stream.stream_name,
                           'arn': instance.Stream.arn,
                           'id':instance.Stream_Details.id,
                           'manifest_file_name':instance.Stream_Details.manifest_file_name,
                           'live':instance.Stream_Details.live,
                           'start_time':instance.Stream_Details.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                           'end_time':instance.Stream_Details.end_time.strftime('%Y-%m-%d %H:%M:%S') if instance.Stream_Details.end_time != None else None
                           })
        else:
            for instance in self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id) \
                    .filter(Camera.id == Stream.camera_id, Stream.id == Stream_Details.stream_id)\
                    .filter(Stream_Details.live == 'True'):
                count = count + 1
                rs.append({'name':instance.Stream.stream_name,
                           'arn': instance.Stream.arn,
                           'id':instance.Stream_Details.id,
                           'manifest_file_name':instance.Stream_Details.manifest_file_name,
                           'live':instance.Stream_Details.live,
                           'start_time':instance.Stream_Details.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                           'end_time':instance.Stream_Details.end_time.strftime('%Y-%m-%d %H:%M:%S') if instance.Stream_Details.end_time != None else None
                           })

        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_stream_details_object(self,query_column,p_object):
        # if start time is found, we need to delete everything in attendant tables and rerun
        # table query does not seem to work with datetime

        if query_column == 'start_time':
            # ensure id and start_time is valid. Otherwise you will get False == 1 or True == 1 crap
            id = p_object.id
            stime = p_object.start_time
            q = self.session.query(Stream_Details)
            q1 = q.filter(Stream_Details.stream_id == id ,Stream_Details.start_time == stime )
            #print(q1)
            instance = q1.first()
            return instance

    def get_stream_details_object1(self,query_column,p_object):
        # if start time is found, we need to delete everything in attendant tables and rerun
        # table query does not seem to work with datetime
        if query_column == 'start_time':
            query_string = " select id  " \
                           "from Stream_Details where stream_id = " + str(p_object.stream_id) +\
                           " and start_time = '" + str(p_object.start_time) + "'"
            instance = self.session.execute(query_string)
            if instance.rowcount == 1:
                for (id ) in instance:
                    inst = self.session.query(Stream_Details).get(id)
                    return inst
        return None

    def get_stream_details_by_time(self,stime,etime):
        # List streams given camera id and time parameters
        count = 0
        rs = []
        stime = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
        etime = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        q = self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id)\
                .filter(Camera.id == Stream.camera_id , Stream.id == Stream_Details.stream_id) \
                .filter(Stream_Details.start_time >= stime, coalesce(Stream_Details.end_time,Stream_Details.start_time) <= etime)
        q1 = str(q.statement.compile(dialect=mysql.dialect()))

        # Use coalesce to set end time to start time for null end times for live events
        for instance in self.session.query(Camera,Stream,Stream_Details).filter(Camera.id== self.id)\
                .filter(Camera.id == Stream.camera_id , Stream.id == Stream_Details.stream_id) \
                .filter(Stream_Details.start_time >= stime, coalesce(Stream_Details.end_time,Stream_Details.start_time) <= etime) :
            count = count + 1
            rs.append({'name':instance.Stream.stream_name,
                       'arn': instance.Stream.arn,
                       'id':instance.Stream_Details.id,
                       'manifest_file_name':instance.Stream_Details.manifest_file_name,
                       'live':instance.Stream_Details.live,
                       'start_time':instance.Stream_Details.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'end_time':instance.Stream_Details.end_time.strftime('%Y-%m-%d %H:%M:%S') if instance.Stream_Details.end_time != None else None
                       })

        rs1 = {'count':count,'result_set':rs}
        return rs1

    def get_stream_details_raw(self,query_column,id):
        # if start time is found, we need to delete everything in attendant tables and rerun
        # table query does not seem to work with datetime
        if query_column == 'max_time':
            query_string = " select max(server_time) " \
                           "from Stream_Details_Raw where stream_details_id = " + str(id)
        elif query_column == 'min_time':
            query_string = " select min(server_time) " \
                           "from Stream_Details_Raw where stream_details_id = " + str(id)

        elif query_column == 'rawfilename':
            query_string = " select producer_time,stream_details_id " \
                           "from Stream_Details_Raw where rawfilename = '" + str(id) + "'"

        if query_column == 'max_rawfilename':
            query_string = " select max(rawfilename) " \
                           "from Stream_Details_Raw where stream_details_id = " + str(id)



        instance = self.session.execute(query_string)
        if instance.rowcount == 1:
            for (mt) in instance:
                return mt



        return None


    def get_stream_metadata_by_time(self,stime,etime,label):
        # List streams given camera id and time parameters
        # TODO need to send back non contigous labels only
        count = 0
        rs = []
        stime = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
        etime = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        label = label.split(',')
        # q = self.session.query(Stream,Stream_Details,Stream_MetaData ).filter(Stream.camera_id== self.id)\
        #         .filter(Stream.id == Stream_Details.stream_id , Stream_Details.id == Stream_MetaData.stream_details_id) \
        #         .filter(Stream_Details.start_time >= stime, Stream_Details.end_time <= etime) \
        #         .filter(Stream_MetaData.label.in_(label))
        # q1 = str(q.statement.compile(dialect=mysql.dialect()))

        for instance in self.session.query(Stream,Stream_Details,Stream_MetaData ).filter(Stream.camera_id== self.id)\
                .filter(Stream.id == Stream_Details.stream_id , Stream_Details.id == Stream_MetaData.stream_details_id) \
                .filter(Stream_Details.start_time >= stime, coalesce(Stream_Details.end_time,Stream_Details.start_time) <= etime) \
                .filter(Stream_MetaData.label.in_(label)):
            count = count + 1
            rs.append({'name':instance.Stream.stream_name,
                       'arn': instance.Stream.arn,
                       'id':instance.Stream_Details.id,
                       'label':instance.Stream_MetaData.label,
                       'manifest_file_name':instance.Stream_Details.manifest_file_name,
                       'live':instance.Stream_Details.live,
                       'label_timestamp':instance.Stream_MetaData.timestamp,
                       # convert decimal to str to make it json serializable
                       'seconds': str(instance.Stream_MetaData.seconds),
                       'start_time':instance.Stream_Details.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'end_time':instance.Stream_Details.end_time.strftime('%Y-%m-%d %H:%M:%S') if instance.Stream_Details.end_time != None else None
                       })

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
        instance = self.session.query(Analytics_MetaData).filter(Analytics_MetaData.camera_id == self.id,
                                                                 Analytics_MetaData.key == key).first()
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
                             resolution = p_object.resolution,
                             start_time = p_object.start_time,
                             end_time = p_object.end_time)
        self.session.add(row)
        self.session.commit()

        return row

    def put_stream_details_raw(self,p_object):
        row = Stream_Details_Raw(stream_details_id=p_object.stream_details_id,
                                 rawfilename=p_object.rawfilename,
                                 server_time = p_object.server_time,
                                 producer_time = p_object.producer_time
                                )
        self.session.add(row)
        self.session.flush()
        self.session.commit()
        return row

    def put_stream_details_ts(self,p_object):
        row = Stream_Details_TS(stream_details_id=p_object.stream_details_id,
                                transportname=p_object.transportname,
                                 server_time = p_object.server_time)
        self.session.add(row)
        self.session.commit()
        return


    def put_stream_metadata(self,p_object):
        row = Stream_MetaData(stream_details_id=p_object.stream_details_id,
                                frame_number=p_object.frame_number,
                                label = p_object.label,
                                confidence = p_object.confidence,
                                position = p_object.position,
                                timestamp = p_object.timestamp,
                                group_id = p_object.group_id,
                                seconds = p_object.seconds)
        self.session.add(row)
        self.session.commit()
        return

    def update_stream_details(self,p_object):
        stmt = update(Stream_Details).where(Stream_Details.id == p_object.id). \
            values(live='False')
        self.session.commit()

    def update_analytics_metaData(self,p_object):
        newval = int(p_object.value) + 1
        p_object.value = str(newval)
        self.session.commit()


def testHarness():
    event = {}
    event['camera_id'] = 1
    event['client_id'] = 1
    event['label'] = 'person,knife'
    event['live'] = 'True'

    # db = database('1')
    # instance = db.get_analytics_metaData_object('raw_file_next_value')
    # db.update_analytics_metaData(instance)

    db = database(1)
    print(db.get_stream_details(event['live']))

    p_object = Object()
    id = 'test_2_rawfile00001000.mkv'
    instance = db.get_stream_details_raw('rawfilename', id)
    print (instance)
    #p_object.id = 1
    p_object.resolution = '1280x720x3'
    p_object.start_time = datetime.datetime.strptime('2018-06-1 9:04:02', '%Y-%m-%d %H:%M:%S')
    #db.put_stream_details(p_object)
    #instance = db.get_stream_details_object1('start_time',p_object)

    print('')

    if 'client_id' in event:
        db = database(event['client_id'])
        body = db.get_client_camera()
        print(json.dumps(body))
        db.close()

    if 'camera_id' in event:
        db = database(event['camera_id'])
        #body = db.get_stream_details()
        #print(json.dumps(body))
        s = '2018-07-11 12:00:00'
        e = '2018-07-12 12:18:30'
        label = event['label']
        body = db.get_stream_details_by_time(s,e)
        print(json.dumps(body))
        db.close()

if __name__ == '__main__':
    testHarness()