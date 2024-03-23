from ninja import Schema

class SuccessOut(Schema):
    success: str = "Task completed successfully"
    code: int = 1

class SuccessData(SuccessOut):
    info: object = {}

class ErrorOut(Schema):
    error: str = "Task failed"
    code: int

class ErrorData(ErrorOut):
    info: object = {}

class AuthenticationIn(Schema):
    username: str
    password: str

class NewUserIn(Schema):
    username: str
    password: str
    email: str
    firstName: str
    lastName: str

class UnrecoverableError(ErrorOut):
    error: str = "Guru Meditation"
    code: int = -1

