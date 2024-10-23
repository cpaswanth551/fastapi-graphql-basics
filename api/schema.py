import asyncio
from typing import List
import strawberry

from api.database import get_db
from api.models import College, Student


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
        """
        Fetches a list of colleges.

        Example query:
        {
          colleges {
            id
            name
            location
          }
        }
        """
        db = next(get_db())
        colleges = db.query(College).all()
        return [
            CollegeType(id=college.id, name=college.name, location=college.location)
            for college in colleges
        ]

    @strawberry.field
    async def students(self) -> List[StudentType]:
        """
        Fetches a list of students.

        Example query:
        {
          students {
            id
            name
            age
            collegeId
          }
        }
        """
        db = next(get_db())
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
    # College CRUD operations
    @strawberry.mutation
    async def create_college(self, name: str, location: str) -> CollegeType:
        """
        Creates a new college.

        Example mutation:
        mutation {
          createCollege(name: "Stanford", location: "California") {
            id
            name
            location
          }
        }
        """
        db = next(get_db())
        college = College(name=name, location=location)
        db.add(college)
        db.commit()
        db.refresh(college)
        return CollegeType(id=college.id, name=college.name, location=college.location)

    @strawberry.mutation
    async def update_college(self, id: int, name: str, location: str) -> CollegeType:
        """
        Updates an existing college.

        Example mutation:
        mutation {
          updateCollege(id: 1, name: "Stanford University", location: "California") {
            id
            name
            location
          }
        }
        """
        db = next(get_db())
        college = db.query(College).filter(College.id == id).first()
        if not college:
            raise ValueError("College not found")
        college.name = name
        college.location = location
        db.commit()
        return CollegeType(id=college.id, name=college.name, location=college.location)

    @strawberry.mutation
    async def delete_college(self, id: int) -> bool:
        """
        Deletes a college by ID.

        Example mutation:
        mutation {
          deleteCollege(id: 1)
        }
        """
        db = next(get_db())
        college = db.query(College).filter(College.id == id).first()
        if college:
            db.delete(college)
            db.commit()
            return True
        return False

    # Student CRUD operations
    @strawberry.mutation
    async def create_student(self, name: str, age: int, college_id: int) -> StudentType:
        """
        Creates a new student.

        Example mutation:
        mutation {
          createStudent(name: "Alice", age: 21, collegeId: 1) {
            id
            name
            age
            collegeId
          }
        }
        """
        db = next(get_db())
        college = db.query(College).filter(College.id == college_id).first()
        if not college:
            raise ValueError("College not found")
        student = Student(name=name, age=age, college_id=college_id)
        db.add(student)
        db.commit()
        db.refresh(student)
        return StudentType(
            id=student.id,
            name=student.name,
            age=student.age,
            college_id=student.college_id,
        )

    @strawberry.mutation
    async def update_student(self, id: int, name: str, age: int) -> StudentType:
        """
        Updates an existing student.

        Example mutation:
        mutation {
          updateStudent(id: 1, name: "Jorge", age: 23) {
            id
            name
            age
          }
        }
        """
        db = next(get_db())
        student = db.query(Student).filter(Student.id == id).first()
        if not student:
            raise ValueError("Student not found")
        student.name = name
        student.age = age
        db.commit()
        return StudentType(
            id=student.id,
            name=student.name,
            age=student.age,
            college_id=student.college_id,
        )

    @strawberry.mutation
    async def delete_student(self, id: int) -> bool:
        """
        Deletes a student by ID.

        Example mutation:
        mutation {
          deleteStudent(id: 4)
        }
        """
        db = next(get_db())
        student = db.query(Student).filter(Student.id == id).first()
        if student:
            db.delete(student)
            db.commit()
            return True
        return False


# GraphQL Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
