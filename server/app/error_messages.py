from flask import Response, json, request

def json_400(reason=None):
    if reason:
        message = reason
    else:
        message = 'Request cannot be fulfilled due to an error.'

    contents = json.dumps({ 'message' : message })
    return Response(contents, 400, mimetype='application/json')

def json_401(reason=None):
    if reason:
        message = reason
    else:
        message = 'Unauthorized request'

    contents = json.dumps({ 'message' : message })
    return Response(contents, 401, mimetype='application/json')

def json_403(reason=None):
    if reason:
        message = reason
    else:
        message = 'Forbidden request'

    contents = json.dumps({ 'message' : message })
    return Response(contents, 403, mimetype='application/json')

def json_410(resource=None):
    if resource:
        message = 'Resource {} does not exist or has been deleted'.format(resource)
    else:
        message = 'This resource does not exist or has been deleted'

    contents = json.dumps({ 'message' : message })
    return Response(contents, 410, mimetype='application/json')

def json_499(reason=None):
    if reason:
        message = reason
    else:
        message = 'Unable to complete request due to server error.'

    contents = json.dumps({ 'message' : message })
    return Response(contents, 499, mimetype='application/json')