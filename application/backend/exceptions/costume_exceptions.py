from fastapi import HTTPException

class StringInsteadOfLetterError(HTTPException):
     def __init__(self, value):
        detail = f"Invalid input: String '{value}' received instead of a letter."
        super().__init__(status_code=403, detail=detail)