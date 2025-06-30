# import os
# import uuid
# from typing import Optional, Type, cast, Protocol
#
# from fastapi import Depends, Request, HTTPException
# from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, exceptions
# from fastapi_users.authentication import AuthenticationBackend, BearerTransport
# from fastapi_users.authentication.strategy import Strategy
# from fastapi_users.db import SQLAlchemyUserDatabase, BaseUserDatabase
# from fastapi_users.jwt import generate_jwt, decode_jwt
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from jose import JWTError
#
# from app.db.db import User, get_async_session
#
# SECRET = os.getenv("SECRET", "default-secret-key")
#
#
# # Define protocol for extended database
# class UserDatabaseWithUsername(BaseUserDatabase[User]):
#     async def get_by_username(self, username: str) -> Optional[User]:
#         ...
#
#
# # Extended user database
# class SQLAlchemyUserDatabaseExtended(SQLAlchemyUserDatabase, UserDatabaseWithUsername):
#     async def get_by_username(self, username: str) -> Optional[User]:
#         statement = select(User).where(User.username == username)
#         result = await self.session.execute(statement)
#         return result.scalar_one_or_none()
#
#
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabaseExtended(session, User)
#
#
# # Custom JWT strategy
# class CustomJWTStrategy(Strategy[User, uuid.UUID]):
#     def __init__(self, secret: str, lifetime_seconds: int, identity_field: str):
#         self.secret = secret
#         self.lifetime_seconds = lifetime_seconds
#         self.identity_field = identity_field
#
#     async def write_token(self, user: User) -> str:
#         data = {"sub": str(getattr(user, self.identity_field))}
#         return generate_jwt(
#             data, self.secret, self.lifetime_seconds
#         )
#
#     async def read_token(
#             self, token: Optional[str], user_manager: BaseUserManager[User, uuid.UUID]
#     ) -> Optional[User]:
#         if token is None:
#             return None
#
#         try:
#             data = decode_jwt(token, self.secret, audience=None)
#             username = data.get("sub")
#             if not username:
#                 return None
#
#             # Get the user by username
#             user_db = user_manager.user_db
#             if hasattr(user_db, 'get_by_username'):
#                 return await user_db.get_by_username(username)
#             return None
#         except (JWTError, KeyError, ValueError):
#             return None
#
#
# # User manager
# class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
#     reset_password_token_secret = SECRET
#     verification_token_secret = SECRET
#
#     @property
#     def user_db(self) -> UserDatabaseWithUsername:
#         return cast(UserDatabaseWithUsername, self._user_db)
#
#     async def create(
#             self,
#             user_create: UserCreate,
#             safe: bool = False,
#             request: Optional[Request] = None,
#     ) -> User:
#         # Validate username
#         if not user_create.username or len(user_create.username) < 3:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Username must be at least 3 characters"
#             )
#
#         # Check for existing username
#         existing_user = await self.user_db.get_by_username(user_create.username)
#         if existing_user:
#             raise exceptions.UserAlreadyExists()
#
#         # Create user
#         user_dict = {
#             "username": user_create.username,
#             "hashed_password": self.password_helper.hash(user_create.password),
#             "email": None,
#             "is_active": True,
#             "is_superuser": False,
#             "is_verified": False
#         }
#
#         created_user = await self.user_db.create(user_dict)
#         await self.on_after_register(created_user, request)
#         return created_user
#
#
# async def get_user_manager(
#         user_db: SQLAlchemyUserDatabaseExtended = Depends(get_user_db),
# ):
#     yield UserManager(user_db)
#
#
# # JWT configuration
# def get_jwt_strategy() -> CustomJWTStrategy:
#     return CustomJWTStrategy(
#         secret=SECRET,
#         lifetime_seconds=60 * 60 * 24,
#         identity_field="username"
#     )
#
#
# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )
#
# fastapi_users = FastAPIUsers[User, uuid.UUID](
#     get_user_manager,
#     [auth_backend],
# )
#
# current_active_user = fastapi_users.current_user(active=True)