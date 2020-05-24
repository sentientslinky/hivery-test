class ParanuaraException(Exception):
    HttpErrorCode = 500
    pass

class InvalidPersonIndexException(ParanuaraException):
    HttpErrorCode = 400

class InvalidCompanyNameException(ParanuaraException):
    HttpErrorCode = 400

class IncorrectParametersException(ParanuaraException):
    HttpErrorCode = 400

class InternalServerIssue(ParanuaraException):
    HttpErrorCode = 500