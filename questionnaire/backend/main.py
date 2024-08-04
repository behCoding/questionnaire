from datetime import timedelta
from typing import List
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

"""# Must be added to add the module packs to the system path if you get import error
import sys
import os
sys.path = ['', '..'] + sys.path[1:]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) """

from questionnaire.backend.database import engine, get_db
from questionnaire.backend.models import Base, User, Form, Question
from questionnaire.backend.auth import authenticate_user, create_access_token, get_password_hash, get_current_user, \
    ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, delete_user, update_user
from questionnaire.backend.serialization import (UserCreate, UserResponse, Token, TokenData, FormResponse, FormCreate,
                                                 QuestionResponse, QuestionCreate, CourseResponse, CourseCreate,
                                                 UserUpdate, CourseBase)
import CRUD as crud

app = FastAPI()

origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8000",  # Backend (optional)
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
Base.metadata.create_all(bind=engine)


@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="A user with this username is already registered in the system")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "user_id": user.id}


@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user.username}"}


@app.post("/courses", response_model=CourseResponse)
def create_course(course: CourseBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized, reach out to the administrator for this operation")
    return crud.create_course(db=db, course=course)


@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course: CourseResponse, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.update_course(db=db, course=course)


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.delete_course(db=db, course_id=course_id)


@app.get("/courses/all", response_model=List[CourseResponse])
def courses_list(db: Session = Depends(get_db)):
    return crud.get_all_courses(db=db)


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return update_user(db=db, user_id=user_id, user=user)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return delete_user(db=db, user_id=user_id)


# Get the courses for a specific teacher
@app.get("/teachers/{teacher_id}/courses", response_model=List[CourseResponse])
def get_teacher_courses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_courses_for_teacher(db=db, teacher_id=current_user.id)


# Add a course to a teacher
@app.post("/teachers/{teacher_id}/courses/{course_id}", response_model=CourseResponse)
def add_course_to_teacher(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.add_course_to_teacher(db=db, teacher_id=current_user.id, course_id=course_id)


@app.post("/courses/{course_id}/forms", response_model=FormResponse)
def create_form(course_id: int, form: FormCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.create_form(db=db, form=form, course_id=course_id, teacher_id=current_user.id)


@app.put("/forms/{form_id}", response_model=FormResponse)
def update_form(form_id: int, form: FormCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_form = db.query(Form).filter(Form.id == form_id).first()
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    if db_form.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for var, value in vars(form).items():
        setattr(db_form, var, value) if value else None
    db.commit()
    db.refresh(db_form)
    return db_form


@app.delete("/forms/{form_id}")
def delete_form(form_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_form = db.query(Form).filter(Form.id == form_id).first()
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    if db_form.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(db_form)
    db.commit()
    return {"message": "Form deleted successfully"}


@app.post("/forms/{form_id}/questions", response_model=QuestionResponse)
def create_question(form_id: int, question: QuestionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_form = db.query(Form).filter(Form.id == form_id).first()
    if db_form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    if db_form.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.create_question(db=db, question=question, form_id=form_id)


@app.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, question: QuestionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    db_form = db.query(Form).filter(Form.id == db_question.form_id).first()
    if db_form.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for var, value in vars(question).items():
        setattr(db_question, var, value) if value else None
    db.commit()
    db.refresh(db_question)
    return db_question


@app.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    db_form = db.query(Form).filter(Form.id == db_question.form_id).first()
    if db_form.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(db_question)
    db.commit()
    return {"message": "Question deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
