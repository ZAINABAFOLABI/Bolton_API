HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_200_NON_AUTHORITATIVE_INFORMATION = 203
HTTP_204_NO_CONTENT = 204
HTTP_205_RESET_CONTENT = 205
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302
HTTP_302_NOT_MODIFIED = 304
HTTP_306_RESERVED = 306
HTTP_307_TEMPORARY_REDIRECT = 307
HTTP_308_PERMANENT_REDIRECT = 308
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORISED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_406_NOT_ACCEPTABLE = 406
HTTP_408_REQUEST_TIMEOUT = 408
HTTP_409_CONFLICT = 409
HTTP_410_GONE = 410
HTTP_411_LENGTH_REQUIRED = 411
HTTP_412_PRECONDITION_FAILED = 412
HTTP_414_REQUEST_URI_TOO_LONG= 414
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
HTTP_423_LOCKED = 423
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_502_BAD_GATEWAY=502
HTTP_503_SERVICE_UNAVAILABLE=503
HTTP_504_GATEWAY_TIMEOUT=504
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED=511

def is_informational(status):
    # 1xx
    pass

def is_success(status):
    # 2xx
    pass

def is_redirect(status):
    # 3xx
    pass

def is_client_error(status):
    # 4xx
    pass

def is_server_error(status):
    # 5xx
    pass







