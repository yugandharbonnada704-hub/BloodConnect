from flask import jsonify

def json_response(status="success", message="", data=None, code=200):
    """
    Standard JSON API response builder.
    status: 'success' or 'error'
    message: descriptive message
    data: dict or list of response payload
    code: HTTP status code
    """
    response = {
        "status": status,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), code

def success_response(message="", data=None, code=200):
    return json_response("success", message, data, code)

def error_response(message="", data=None, code=400):
    return json_response("error", message, data, code)
