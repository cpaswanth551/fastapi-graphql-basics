from fastapi import FastAPI
from strawberry.asgi import GraphQL

from schema import schema
from models import Base
from database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def index():
    return {"message": "hello world !"}


app.add_route("/graphql", GraphQL(schema=schema))
