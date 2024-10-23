
# College and Student Management API

## Overview

This repository contains a GraphQL API for managing colleges and students. Built with Python, Strawberry GraphQL, and SQLAlchemy, it allows users to perform CRUD (Create, Read, Update, Delete) operations efficiently.

## What is GraphQL?

GraphQL is a query language for APIs that enables clients to request exactly the data they need. Unlike REST, which exposes multiple endpoints for different resources, GraphQL provides a single endpoint for all operations.

### Key Features of GraphQL:

- **Single Endpoint**: All requests are made to a single URL.
- **Client-Specified Queries**: Clients can specify the exact shape of the data they need.
- **Strongly Typed Schema**: The API schema defines types and relationships, ensuring data integrity.

## API Implementation

### Code Structure

Here's the core implementation of the API:

#### 1. Define Data Types

We define two data types: `CollegeType` and `StudentType`.

```python
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
````

These types represent the structure of the college and student data.

#### 2. Query Section

The `Query` class handles fetching data.

```python
@strawberry.type
class Query:
    @strawberry.field
    async def colleges(self) -> List[CollegeType]:
        db = next(get_db())
        colleges = db.query(College).all()
        return [
            CollegeType(id=college.id, name=college.name, location=college.location)
            for college in colleges
        ]

    @strawberry.field
    async def students(self) -> List[StudentType]:
        db = next(get_db())
        students = db.query(Student).all()
        return [
            StudentType(id=student.id, name=student.name, age=student.age, college_id=student.college_id)
            for student in students
        ]
```

- **`colleges`**: Retrieves a list of all colleges.
- **`students`**: Retrieves a list of all students.

### Example Query: Fetch Colleges

**GraphQL Query**:

```graphql
{
  colleges {
    id
    name
    location
  }
}
```

**Example Output**:

```json
{
  "data": {
    "colleges": [
      {
        "id": 1,
        "name": "Stanford",
        "location": "California"
      },
      {
        "id": 2,
        "name": "Harvard",
        "location": "Massachusetts"
      }
    ]
  }
}
```

### 3. Mutation Section

The `Mutation` class handles data modifications.

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
```

- **`create_college`**: Adds a new college to the database.

### Example Mutation: Create College

**GraphQL Mutation**:

```graphql
mutation {
  createCollege(name: "Stanford", location: "California") {
    id
    name
    location
  }
}
```

**Example Output**:

```json
{
  "data": {
    "createCollege": {
      "id": 3,
      "name": "Stanford",
      "location": "California"
    }
  }
}
```

### 4. Additional Mutations

Similarly, you can define additional mutations for updating and deleting colleges and students.

- **Update College**:

```python
@strawberry.mutation
async def update_college(self, id: int, name: str, location: str) -> CollegeType:
    db = next(get_db())
    college = db.query(College).filter(College.id == id).first()
    if not college:
        raise ValueError("College not found")
    college.name = name
    college.location = location
    db.commit()
    return CollegeType(id=college.id, name=college.name, location=college.location)
```

**Example Mutation**:

```graphql
mutation {
  updateCollege(id: 1, name: "Stanford University", location: "California") {
    id
    name
    location
  }
}
```

**Example Output**:

```json
{
  "data": {
    "updateCollege": {
      "id": 1,
      "name": "Stanford University",
      "location": "California"
    }
  }
}
```

### 5. Running the API

#### Prerequisites

- Python 3.7 or higher
- Required packages:
  ```bash
  pip install strawberry-graphql sqlalchemy
  ```

#### Database Setup

Ensure your database is set up and the models (`College` and `Student`) are defined in `models.py`. Update the `get_db` function to connect to your database.

#### Starting the Server

1. **Run the API with Uvicorn**:
   Open a terminal and execute:

   ```bash
   uvicorn your_module_name:app --reload
   ```

   Replace `your_module_name` with the name of your Python file containing the API code.

2. **Access GraphQL Playground**:
   Open your web browser and navigate to `http://localhost:8000/graphql`. This will open the GraphQL playground where you can execute your queries and mutations.

## Conclusion

This API offers a robust way to manage college and student records using GraphQL. You can easily extend it to add more features as needed. For any questions or contributions, feel free to open an issue or submit a pull request!

```
