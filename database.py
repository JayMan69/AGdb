from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import rds_config
from create_tables import  Client

Base = declarative_base()

connection_string = "mysql://"+rds_config.db_username+':'+rds_config.db_password+ '@' +\
                    rds_config.db_endpoint+':'+ str(rds_config.db_port) +'/' + rds_config.db_name

engine = create_engine(connection_string)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert a Person in the person table
new_person = Client(name='Armour Grid')
session.add(new_person)
session.commit()

