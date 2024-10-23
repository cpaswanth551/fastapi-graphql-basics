Here is a **complete `README.md`** with **CRUD operations, subscriptions, testing instructions**, and details to build a full **GraphQL API** using **Strawberry** and **SQLAlchemy** from start to finish.

---

# GraphQL API with Strawberry, SQLAlchemy, and Subscriptions

This project demonstrates how to build a **GraphQL API** using **Strawberry** with **SQLAlchemy** for database interaction. It provides complete **CRUD operations** and **subscriptions**, including setup instructions and testing methods.

---

## Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.7+**
- **SQLAlchemy** – ORM for database interaction
- **Strawberry** – GraphQL library for Python
- **Uvicorn** – ASGI server for serving the GraphQL API
- **Websockets** – For handling subscriptions

### Install Dependencies

You can install all the necessary dependencies with:

```bash
pip install strawberry-graphql sqlalchemy uvicorn websockets
```

---

## Project Structure

- **`database.py`**: Contains the database connection logic using SQLAlchemy.
- **`models.py`**: Defines the SQLAlchemy models (`College` and `Student`).
- **`main.py`**: Implements the **GraphQL schema**, including queries, mutations, and subscriptions.
- **`tests.py`**: Provides tests for the API's queries and mutations.

---

## 1. Database Setup

Create a **SQLite** database or configure another relational database (e.g., PostgreSQL, MySQL) in `database.py`. Example:

**`database.py`**:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 2. Models Definition

Define the models for **College** and **Student** using SQLAlchemy in `models.py`.

**`models.py`**:

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)

    students = relationship("Student", back_populates="college")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    college_id = Column(Integer, ForeignKey("colleges.id"))

    college = relationship("College", back_populates="students")
```

---

## 3. GraphQL Types and Schema

Create **GraphQL types**, **queries**, **mutations**, and **subscriptions** in `main.py`.

### GraphQL Types

```python
import strawberry

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
```

---

### Query Section

Define queries to **retrieve data** from the database.

```python
from typing import List
from database import get_db
from models import College, Student

@strawberry.type
class Query:
    @strawberry.field
    async def colleges(self) -> List[CollegeType]:
        db = next(get_db())
        colleges = db.query(College).all()
        return [CollegeType(id=c.id, name=c.name, location=c.location) for c in colleges]

    @strawberry.field
    async def students(self) -> List[StudentType]:
        db = next(get_db())
        students = db.query(Student).all()
        return [
            StudentType(id=s.id, name=s.name, age=s.age, college_id=s.college_id)
            for s in students
        ]
```

---

### Mutation Section

Define **mutations** to **create, update, and delete** data.

```python
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_college(self, name: str, location: str) -> CollegeType:
        db = next(get_db())
        college = College(name=name, location=location)
        db.add(college)
        db.commit()
        db.refresh(college)
        return CollegeType(id=college.id, name=college.name, location=college.location)

    @strawberry.mutation
    async def create_student(self, name: str, age: int, college_id: int) -> StudentType:
        db = next(get_db())
        student = Student(name=name, age=age, college_id=college_id)
        db.add(student)
        db.commit()
        db.refresh(student)
        return StudentType(id=student.id, name=student.name, college_id=college_id)

    @strawberry.mutation
    async def delete_student(self, id: int) -> bool:
        db = next(get_db())
        student = db.query(Student).filter(Student.id == id).first()
        if student:
            db.delete(student)
            db.commit()
            return True
        return False
```

---

### Subscription Section

Add a **subscription** to notify when a new college is added.

```python
from asyncio import Queue

class Subscription:
    college_queue = Queue()

    @strawberry.subscription
    async def on_new_college(self) -> CollegeType:
        while True:
            college = await self.college_queue.get()
            yield college

    @staticmethod
    async def notify_new_college(college: CollegeType):
        await Subscription.college_queue.put(college)
```

Modify the `create_college` mutation to **notify subscribers**.

```python
    @strawberry.mutation
    async def create_college(self, name: str, location: str) -> CollegeType:
        db = next(get_db())
        college = College(name=name, location=location)
        db.add(college)
        db.commit()
        db.refresh(college)

        college_type = CollegeType(id=college.id, name=college.name, location=college.location)
        await Subscription.notify_new_college(college_type)
        return college_type
```

---

### Schema Definition

Combine the **query, mutation, and subscription** into a schema.

```python
schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
```

---

## 4. Running the API

Run the API using **Uvicorn**:

```bash
uvicorn main:app --reload
```

Access the GraphQL Playground at [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql).

---

## 5. Example Queries and Mutations

### Query Example

```graphql
query {
  colleges {
    id
    name
    location
  }
}
```

### Mutation Example

```graphql
mutation {
  createCollege(name: "Harvard", location: "Massachusetts") {
    id
    name
    location
  }
}
```

### Subscription Example

```graphql
subscription {
  onNewCollege {
    id
    name
    location
  }
}
```

---

## 6. Testing the API

Create a `tests.py` file to test your GraphQL queries and mutations.

**`tests.py`**:

```python
import requests

def test_create_college():
    query = """
    mutation {
      createCollege(name: "Test College", location: "Test Location") {
        id
        name
      }
    }
    """
    response = requests.post("http://127.0.0.1:8000/graphql", json={"query": query})
    assert response.status_code == 200

if __name__ == "__main__":
    test_create_college()
    print("Test passed!")
```

Run the tests:

```bash
python tests.py
```

---

## 7. License

This project is licensed under the MIT License.

---

This **README** provides a complete overview of the GraphQL API using Strawberry, SQLAlchemy, and Uvicorn, including setup, CRUD operations, subscriptions, and testing.
