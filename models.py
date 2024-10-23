from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    college_id = Column(Integer, ForeignKey("colleges.id"))
