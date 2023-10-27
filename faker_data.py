from random import random, randint
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

fake = Faker('uk')

# Підключення до бази данх
engine = create_engine('sqlite:///homework7.db', echo=True)
Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group")
    grades = relationship("Grade")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    student_id = Column(Integer, ForeignKey('students.id'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

groups = [Group(name=fake.unique.random_element(("ET-22", "MR-22", "MN-22"))) for _ in range(3)]
session.add_all(groups)

teachers = [Teacher(name=fake.unique.name()) for _ in range(5)]
session.add_all(teachers)

subjects = [Subject(name=fake.random_element(("Math", "Physics", "Chemistry", "History", "Biology")),
                    teacher=fake.random_element(teachers)) for _ in range(7)]
session.add_all(subjects)

students = [Student(name=fake.unique.name(), group=fake.random_element(groups)) for _ in range(50)]
session.add_all(students)

for student in range(50):
    for subject in range(20):
        grades = Grade(value=randint(2, 5), student_id=student+1, subject_id=randint(1,7))

        session.add(grades)
print()
session.commit()

session.close()