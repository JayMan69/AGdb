import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import rds_config
from create_tables import  Client


def hello(event, context):
    body = {
        "message": "Test1",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    Base = declarative_base()

    connection_string = "mysql://" + rds_config.db_username + ':' + rds_config.db_password + '@' + \
                        rds_config.db_endpoint + ':' + str(rds_config.db_port) + '/' + rds_config.db_name

    engine = create_engine(connection_string)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Insert a Person in the person table
    new_person = Client(name='Armour Grid3')
    session.add(new_person)
    session.commit()

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

