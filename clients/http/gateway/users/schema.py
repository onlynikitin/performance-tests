from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    """Данные пользователя в ответе API."""

    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class GetUserResponseSchema(BaseModel):
    """Ответ получения пользователя."""

    user: UserSchema


class CreateUserRequestSchema(BaseModel):
    """Данные запроса создания пользователя."""

    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class CreateUserResponseSchema(BaseModel):
    """Ответ создания пользователя."""

    user: UserSchema
