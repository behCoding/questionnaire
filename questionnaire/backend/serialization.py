from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class FormBase(BaseModel):
    title: str


class FormCreate(FormBase):
    pass


class FormResponse(FormBase):
    id: int
    course_id: int
    teacher_id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    form_id: int

    class Config:
        orm_mode = True


class ResponseCreate(BaseModel):
    question_id: int
    selected_option: str


class ResponseResponse(BaseModel):
    id: int
    form_id: int
    student_id: int
    question_id: int
    selected_option: str

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]