from sqlalchemy.orm import Session
from questionnaire.backend.models import User, Form, Question, Course
from questionnaire.backend.serialization import FormCreate, QuestionCreate, CourseCreate, CourseBase, CourseResponse


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_course(db: Session, course: CourseBase):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_all_courses(db: Session):
    return db.query(Course).all()


def update_course(db: Session, course: CourseResponse):
    db_course = db.query(Course).filter(Course.id == course.id).first()
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


def get_courses_for_teacher(db: Session, teacher_id: int):
    return db.query(Course).join(Form).filter(Form.teacher_id == teacher_id).all()


def add_course_to_teacher(db: Session, teacher_id: int, course_id: int):
    teacher_course = Form(teacher_id=teacher_id, course_id=course_id)
    db.add(teacher_course)
    db.commit()
    return db.query(Course).filter(Course.id == course_id).first()


def create_question(db: Session, question: QuestionCreate, form_id: int):
    db_question = Question(**question.dict(), form_id=form_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
