from rest_framework.exceptions import APIException

class TransferException(APIException):
    status_code = 400

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = "Money transfer error."
        super().__init__(detail=detail, code=code)
