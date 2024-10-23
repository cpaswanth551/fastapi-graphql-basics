import asyncio
from typing import AsyncGenerator, List
import strawberry

from database import get_db
from models import College, Student


@strawberry.type
class CollegeType:
    id: int
    name: str
    location: str


@strawberry.type
class StudentType:
    id: int
    name: str
    age: int
    college_id: int


# Query section


@strawberry.type
class Query:
    @strawberry.field
    async def colleges(self) -> List[CollegeType]:
        db = get_db()
        colleges = db.query(College).all()
        return [
            CollegeType(id=college.id, name=college.name, location=college.location)
            for college in colleges
        ]

    async def students(self) -> List[StudentType]:
        db = get_db()
        students = db.query(Student).all()
        return [
            StudentType(
                id=student.id,
                name=student.name,
                age=student.age,
                college_id=student.college_id,
            )
            for student in students
        ]


# Mutation section


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_college(self, name: str, location: str) -> StudentType:
        db = get_db()
        college = College(name=name, location=location)
        db.add(college)
        db.commit()
        db.refresh(college)
        return College(id=college.id, name=college.name, location=college.location)

    @strawberry.mutation
    async def create_student(self, name: str, age: int, college_id: int) -> StudentType:
        db = get_db()
        college = db.query(College).filter(College.id == college_id).first()
        if not college:
            raise ValueError("college not found")
        student = Student(name=name, age=age, college_id=college_id)
        db.add(student)
        db.commit()
        db.refresh(student)
        return StudentType(
            id=student.id, name=student.name, college_id=student.college_id
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
