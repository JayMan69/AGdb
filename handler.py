import json
from database import database


def clients(event, context):

    if 'client_id' in event['headers']:
        db = database(event['headers']['client_id'])
        body = db.get_client()
    else:
        db = database()
        body = db.get_clients()

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }


    return response


def cameras(event, context):

    if 'camera_id' in event['headers']:
        db = database(event['headers']['camera_id'])
        body = db.get_camera()
    else:
        db = database()
        body = db.get_cameras()

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }


    return response

def client_cameras(event, context):

    if 'client_id' in event['headers']:
        db = database(event['headers']['client_id'])
        body = db.get_client_camera()
    else:
        ""
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }


    return response


def streams(event, context):

    if 'camera_id' in event['headers']:
        db = database(event['headers']['camera_id'])
        body = db.get_stream()
    else:
        body = ''

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }


    return response

def stream_details(event, context):

    if 'camera_id' in event['headers']:
        db = database(event['headers']['camera_id'])
        if 'start_time' in event['headers'] and 'end_time' in event['headers']:
            stime = event['headers']['start_time']
            etime = event['headers']['end_time']
            body = db.get_stream_details_by_time(stime,etime)
        else:
            body = db.get_stream_details()
    else:
        body = ''

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }


    return response

def stream_metadata(event, context):

    if 'camera_id' in event['headers']:
        db = database(event['headers']['camera_id'])
        if 'start_time' in event['headers'] and 'end_time' in event['headers']:
            stime = event['headers']['start_time']
            etime = event['headers']['end_time']
            if 'label' in event['headers']:
                label = event['headers']['label']
                body = db.get_stream_metadata_by_time(stime, etime,label)
            else:
                body = ''
        else:
            body = ''
    else:
        body = ''

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }


    return response


