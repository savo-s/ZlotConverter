from fastapi import Depends, FastAPI
from dotenv import load_dotenv
from app.db.db import create_db_and_tables, User
from app.db.schemas import UserCreate, UserRead, UserUpdate
from app.db.users import auth_backend, current_active_user, fastapi_users

app = FastAPI(title="FastAPI-Users + SQLite example")


async def initialize_database():
    await create_db_and_tables()
    print("Database and tables created")

# -------- Auth & User routes --------------------------------------------------
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Password reset & e-mail verification (optional but handy)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

# CRUD endpoints for the *current* user
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


# -------- Public demo route ---------------------------------------------------
@app.get("/hello")
async def hello():
    return {"msg": "Hello!"}


# -------- Start-up hook -------------------------------------------------------
@app.on_event("startup")
async def on_startup():
    await initialize_database()
