from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from src.database.connection import create_db_and_tables
from src.auth.models import User
from src.auth.service import current_active_user
from src.auth.routes import auth_router
from src.auth.schemas import UserRead, UserUpdate
from src.auth.service import fastapi_users

version: str = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Bookly",
    description="A REST API for book review web service",
    version=version,
)


app.include_router(
    auth_router,
    prefix=f"/api/{version}/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=f"/api/{version}/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
