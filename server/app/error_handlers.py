from flask import request, Response, json
from app import app

@app.errorhandler(401)
def page_not_found(e):
    title = "401 - {}".format(e.name)
    message = "Unauthorized {}".format(request.url)
    return 401

@app.errorhandler(403)
def page_not_found(e):
    title = "403 - {}".format(e.name)
    message = "Forbidden {}".format(request.url)
    return 403

@app.errorhandler(404)
def page_not_found(e):
    title = "404 - {}".format(e.name)
    message = "Could not find page at {}".format(request.url)
    return 404

@app.errorhandler(500)
def internal_error(e):
    title = "500 - Internal Server Error"
    message = "On {} {}\n{}".format(request.method, request.url, e)
    return Response(json.dumps({}), 500, mimetype='application/json')