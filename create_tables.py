import os
import sys
from AGdb.rds_config import db_username,db_password,db_endpoint,db_port,db_name
from sqlalchemy import Column, ForeignKey, Integer, String , DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Client(Base):
    __tablename__ = 'Client'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Camera(Base):
    __tablename__ = 'Camera'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Client_Cameras(Base):
    __tablename__ = 'Client_Cameras'
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey('Camera.id'))
    camera = relationship(Camera)
    client_id = Column(Integer, ForeignKey('Client.id'))
    client = relationship(Client)

class Stream(Base):
    __tablename__ = 'Stream'
    id = Column(Integer, primary_key=True)
    stream_name = Column(String(250), nullable=False)
    arn = Column(String(250), nullable=False)
    region = Column(String(250), nullable=False)
    camera_id = Column(Integer, ForeignKey('Camera.id'))
    camera = relationship(Camera)


class Stream_Details(Base):
    __tablename__ = 'Stream_Details'
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer, ForeignKey('Stream.id'))
    stream = relationship(Stream)
    # manifest_file_name can be filled in later
    manifest_file_name = Column(String(250), nullable=True)
    # True / False
    live = Column(String(10), nullable=True)
    # 640x320x3
    resolution = Column(String(250), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

class Stream_MetaData(Base):
    __tablename__ = 'Stream_MetaData'
    id = Column(Integer, primary_key=True)
    stream_details_id = Column(Integer, ForeignKey('Stream_Details.id'))
    stream = relationship(Stream_Details)
    frame_number = Column(Integer, nullable=False)
    label = Column(String(250), nullable=False)
    confidence = Column(String(250), nullable=True)
    position = Column(String(250), nullable=True)
    timestamp = Column(String(250), nullable=True)
    # foreign key constraint is created as an alter table statement below
    stream_details_ts_id = Column(Integer)

class Stream_Details_Raw(Base):
    __tablename__ = 'Stream_Details_Raw'
    id = Column(Integer, primary_key=True)
    stream_details_id = Column(Integer, ForeignKey('Stream_Details.id'))
    stream = relationship(Stream_Details)
    # create index for rawfile to enable search
    rawfilename = Column(String(250), index=True,nullable=False)
    server_time = Column(DateTime, index=True,nullable=False)
    producer_time = Column(DateTime, index=True, nullable=False)

class Stream_Details_TS(Base):
    __tablename__ = 'Stream_Details_TS'
    id = Column(Integer, primary_key=True)
    stream_details_id = Column(Integer, ForeignKey('Stream_Details.id'))
    stream = relationship(Stream_Details)
    # create index for TS to enable search
    transportname = Column(String(250), index=True,nullable=False)
    server_time = Column(DateTime, index=True,nullable=False)

class Analytics_MetaData(Base):
    __tablename__ = 'Analytics_MetaData'
    id = Column(Integer, primary_key=True)
    key = Column(String(250), index=True,nullable=False)
    value = Column(String(250), index=True,nullable=False)
    camera_id = Column(Integer, ForeignKey('Camera.id'))
    camera = relationship(Camera)

# added 6/14
stream_metadata_label_index = Index('stream_metadata_label_index', Stream_MetaData.label)
stream_details_time_index = Index('stream_details_time_index', Stream_Details.start_time,Stream_Details.end_time)

# added 6/15
statments = []
# statments.append('ALTER TABLE Stream_MetaData ADD column stream_details_ts_id int')
#
# statments.append( 'ALTER TABLE Stream_MetaData ADD CONSTRAINT Stream_MetaData_self_1 ' \
#               'FOREIGN KEY(stream_details_ts_id) REFERENCES Stream_Details_TS (id)')



if __name__ == '__main__':
    print('In main of create_tables')
    connection_string = "mysql://"+db_username+':'+db_password+ '@' +\
                        db_endpoint+':'+ str(db_port) +'/' + db_name
    engine = create_engine(connection_string)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    # added 6/14. Need to comment the indexes or put in try catch blocks!!!
    #stream_metadata_label_index.create(bind=engine)
    #stream_details_time_index.create(bind=engine)

    # added 6/15
    for line in statments:
        engine.execute(line)
