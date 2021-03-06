import json
# note no need of putting AGdb.database for import
from database import database


def clients(event, context):

    if 'headers' in event:
        if 'client_id' in event['headers']:
            db = database(event['headers']['client_id'])
            body = db.get_client()
            db.close()
        else:
            db = database()
            body = db.get_clients()
            db.close()
    else:
        if 'client_id' in event:
            db = database(event['client_id'])
            body = db.get_client()
            db.close()
        else:
            db = database()
            body = db.get_clients()
            db.close()


    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": { "Access-Control-Allow-Origin": "*", # Required for CORS support to work
                     "Access-Control-Allow-Credentials": True # Required for cookies, authorization headers with HTTPS
                    },
    }


    return response


def cameras(event, context):

    if 'headers' in event:
        if 'camera_id' in event['headers']:
            db = database(event['headers']['camera_id'])
            body = db.get_camera()
            db.close()
        else:
            db = database()
            body = db.get_cameras()
            db.close()
    else:
        if 'camera_id' in event:
            db = database(event['camera_id'])
            body = db.get_camera()
            db.close()
        else:
            db = database()
            body = db.get_cameras()
            db.close()


    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                    "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
                    },

    }


    return response

def client_cameras(event, context):

    if 'headers' in event:
        if 'client_id' in event['headers']:
            db = database(event['headers']['client_id'])
            body = db.get_client_camera()
            db.close()
        else:
            body = "client_id not present in headers"
        response = {
            "statusCode": 200,
            "body": json.dumps(body),
            "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                        "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
                        },
        }
    else:
        if 'client_id' in event:
            db = database(event['client_id'])
            body = db.get_client_camera()
            db.close()
        else:
            body = "client_id not present in headers"
        response = {
            "statusCode": 200,
            "body": json.dumps(body),
            "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                        "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
                        },
        }


    return response


def streams(event, context):
    if 'headers' in event:
        if 'camera_id' in event['headers']:
            db = database(event['headers']['camera_id'])
            body = db.get_stream()
            db.close()
        else:
            body = 'camera_id not present in headers'

        response = {
            "statusCode": 200,
            "body": json.dumps(body),
            "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                        "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
                        },
        }
    else:
        if 'camera_id' in event:
            db = database(event['camera_id'])
            body = db.get_stream()
            db.close()
        else:
            body = 'camera_id not present in headers'

        response = {
            "statusCode": 200,
            "body": json.dumps(body),
            "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                        "Access-Control-Allow-Credentials": True
                        # Required for cookies, authorization headers with HTTPS
                        },
        }

    return response

def stream_details(event, context):
    if 'headers' in event:
        if 'camera_id' in event['headers']:
            db = database(event['headers']['camera_id'])
            if 'live' in event['headers']:
                body = db.get_stream_details(event['headers']['live'])
            else:
                if 'start_time' in event['headers'] and 'end_time' in event['headers']:
                    stime = event['headers']['start_time']
                    etime = event['headers']['end_time']
                    body = db.get_stream_details_by_time(stime,etime)
                else:
                    body = db.get_stream_details()
            db.close()
        else:
            body = 'camera_id not present in headers'
    else:
        if 'camera_id' in event:
            db = database(event['camera_id'])
            if 'live' in event:
                body = db.get_stream_details(event['live'])
            else:
                if 'start_time' in event and 'end_time' in event:
                    stime = event['start_time']
                    etime = event['end_time']
                    body = db.get_stream_details_by_time(stime,etime)
                else:
                    body = db.get_stream_details()
            db.close()
        else:
            body = 'camera_id not present in headers'


    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                    "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
                    },
    }


    return response

def stream_metadata(event, context):
    if 'headers' in event:
        if 'camera_id' in event['headers']:
            db = database(event['headers']['camera_id'])
            if 'start_time' in event['headers'] and 'end_time' in event['headers']:
                stime = event['headers']['start_time']
                etime = event['headers']['end_time']
                if 'label' in event['headers']:
                    label = event['headers']['label']
                    body = db.get_stream_metadata_by_time(stime, etime,label)
                else:
                    body = 'label not present in headers'
            else:
                body = 'start_time or end_time not present in headers'
            db.close()
        else:
            body = 'camera_id not present in headers'
    else:
        if 'camera_id' in event:
            db = database(event['camera_id'])
            if 'start_time' in event and 'end_time' in event:
                stime = event['start_time']
                etime = event['end_time']
                if 'label' in event:
                    label = event['label']
                    body = db.get_stream_metadata_by_time(stime, etime,label)
                else:
                    body = 'label not present in headers'
            else:
                body = 'start_time or end_time not present in headers'
            db.close()
        else:
            body = 'camera_id not present in headers'


    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                    "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
                    },
    }


    return response


def server_metadata(event, context):
    import datetime
    from time import gmtime, strftime
    body = {'servertime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'servertimezone':strftime("%Z", gmtime())}


    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {"Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                    "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
                    },
    }
    return response