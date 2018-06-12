import os
import sys
import rds_config
from sqlalchemy import Column, ForeignKey, Integer, String , DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Client(Base):
    __tablename__ = 'Client'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Camera(Base):
    __tablename__ = 'Camera'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    camera_id = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)

class Client_Cameras(Base):
    __tablename__ = 'Client_Cameras'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey('Camera.id'))
    camera = relationship(Camera)
    client_id = Column(Integer, ForeignKey('Client.id'))
    client = relationship(Client)

class Stream(Base):
    __tablename__ = 'Stream'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    stream_name = Column(String(250), nullable=False)
    arn = Column(String(250), nullable=False)
    camera_id = Column(Integer, ForeignKey('Camera.id'))
    camera = relationship(Camera)


class Stream_Details(Base):
    __tablename__ = 'Stream_Details'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer, ForeignKey('Stream.id'))
    stream = relationship(Stream)
    manifest_file_name = Column(String(250), nullable=False)
    resolution = Column(String(250), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

class Stream_MetaData(Base):
    __tablename__ = 'Stream_MetaData'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    stream_details_id = Column(Integer, ForeignKey('Stream_Details.id'))
    stream = relationship(Stream_Details)
    frame_number = Column(Integer, nullable=False)
    label = Column(String(250), nullable=False)
    confidence = Column(String(250), nullable=True)
    position = Column(String(250), nullable=True)




connection_string = "mysql://"+rds_config.db_username+':'+rds_config.db_password+ '@' +\
                    rds_config.db_endpoint+':'+ str(rds_config.db_port) +'/' + rds_config.db_name
engine = create_engine(connection_string)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
#Base.metadata.create_all(engine)