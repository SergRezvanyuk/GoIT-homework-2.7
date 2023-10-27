from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from models import Student, Group, Teacher, Subject, Grade

engine = create_engine('sqlite:///homework7.db')

Session = sessionmaker(bind=engine)
session = Session()

# Запит 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    query = (
        session.query(Student.name, func.avg(Grade.value).label('average_grade'))
        .join(Grade)
        .group_by(Student)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
    )
    result = query.all()
    return result

# Запит 2: Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    query = (
        session.query(Student.name, func.avg(Grade.value).label('average_grade'))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student)
        .order_by(func.avg(Grade.value).desc())
        .limit(1)
    )
    result = query.first()
    return result

# Запит 3: Знайти середній бал у групах з певного предмета.
def select_3(subject_name):

    subject = session.query(Subject).filter(Subject.name == subject_name).first()

    if subject:
        grades = session.query(Grade).filter(Grade.subject_id == subject.id).all()
        total_grades = [grade.value for grade in grades]
        average_grade = sum(total_grades) / len(total_grades)
        return average_grade


# Запит 4: Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    query = session.query(func.avg(Grade.value).label('average_grade'))
    result = query.scalar()
    return result

# Запит 5: Знайти, які курси читає певний викладач.
def select_5(teacher_name):
    query = (
        session.query(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
    )
    result = [subject.name for subject in query.all()]
    return result

# Запит 6: Знайти список студентів у певній групі.
def select_6(group_name):
    query = (
        session.query(Student)
        .join(Group)
        .filter(Group.name == group_name)
    )
    result = [student.name for student in query.all()]
    return result

# Запит 7: Знайти оцінки студентів в окремій групі з певного предмета.
def select_7(group_name, subject_name):
    query = (
        session.query(Student.name, Grade.value)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
    )
    result = query.all()
    return result

# Запит 8: Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_name):
    query = (
        session.query(func.avg(Grade.value).label('average_grade'))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
    )
    result = query.scalar()
    return result

# Запит 9: Знайти список курсів, які відвідує певний студент.
def select_9(student_name):
    query = (
        session.query(Subject)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
    )
    result = [subject.name for subject in query.all()]
    return result

# Запит 10: Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    query = (
        session.query(Subject)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
    )
    result = [subject.name for subject in query.all()]
    return result


# result1 = select_1()
# result2 = select_2('Філософія')
# result3 = select_3('Філософія')
# result4 = select_4()
# result5 = select_5('Юстина Чарниш')
# result6 = select_6('ET-22')
# result7 = select_7('ET-22', 'Математичний аналіз')
# result8 = select_8('Михайло Франчук')
# result9 = select_9('Данна Гузій')
# result10 = select_10('Михайлина Рудик', 'Тетяна Засядько')

# print(result10)

session.close()