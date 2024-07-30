from sqlalchemy.orm import Session
from questionnaire.backend.models import User, Form, Question
from questionnaire.backend.serialization import FormCreate, QuestionCreate


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


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
