from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "Antis",
                "email": "antantas123@gmail.com",
                "password": "1234",
            }
        }


class AccountResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "Antis",
                "email": "antantas123@gmail.com",
                "password": "1234",

            }
        }


class AccountUpdate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "Antis",
                "email": "antantas123@gmail.com",
                "password": "1234",
            }
        }
