from sqlalchemy.orm import Session
from questionnaire.backend.models import User, Form, Question, Course
from questionnaire.backend.serialization import FormCreate, QuestionCreate, CourseCreate


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course: CourseCreate):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        for var, value in vars(course).items():
            setattr(db_course, var, value) if value else None
        db.commit()
        db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course


def create_form(db: Session, form: FormCreate, course_id: int, teacher_id: int):
    db_form = Form(**form.dict(), course_id=course_id, teacher_id=teacher_id)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form


def create_question(db: Session, question: QuestionCreate, form_id: int):
    db_question = Question(**question.dict(), form_id=form_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
