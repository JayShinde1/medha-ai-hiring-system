from pydantic import BaseModel, EmailStr, field_validator

class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str

    @field_validator('role')
    @classmethod
    def role_validator(cls, value):
        valid_roles = ['recruiter', 'candidate']

        if value not in valid_roles:
            raise ValueError("Invalid role")

        return value


class Token(BaseModel):
    access_token: str
    token_type: str