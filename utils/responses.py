class ResponseMessageDict:
    RESP_NOTAUTH = {"message": "Missing authorization header from request, or it was invalid"}
    RESP_FORBID = {"message": "You do not have permissions for this action"}
    RESP_URLARG = {"message": "URL arg '{}' expects type {}, got type '{}' instead"}
    RESP_SRVERR = {"message": "An internal server error occurred"}
    RESP_USRNTF = {"message": "User was not found"}
    RESP_USRBSC = {"message": "User is not a verified member of vRCAF"}


class InternalMessageStrings:
    TYPE_DBLRET = ""