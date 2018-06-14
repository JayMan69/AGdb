import json
import database

def clients(event, context):

    if 'client_id' in event:
        db = database(event['client_id'])
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

    if 'camera_id' in event:
        db = database(event['client_id'])
        body = db.get_camera()
    else:
        db = database()
        body = db.get_cameras()

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }


    return response
