class CustomException(Exception):
    message = 'custom message'

class InvalidSquare(CustomException):
    message = 'invalid square'

class InvalidSymbol(CustomException):
    message = 'invalid symbol'

class NonEmptySquare(CustomException):
    message = 'square is not empty'



