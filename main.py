import logging

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from app.db.database import create_db_and_tables
from app.routers import auth, users, wallets

# --------------------------------------------------------------------------- #
#  Logging
# --------------------------------------------------------------------------- #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
#  FastAPI application
# --------------------------------------------------------------------------- #
app = FastAPI(
    title="ZlotConverter API",
    description="Currency conversion and wallet management API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

# --------------------------------------------------------------------------- #
#  Security – HTTP Bearer (JWT)
# --------------------------------------------------------------------------- #
security_scheme = HTTPBearer(
    scheme_name="BearerAuth",            # label in Swagger UI
    bearerFormat="JWT",
    description="Paste your JWT token here:",
)


# --------------------------------------------------------------------------- #
#  Custom OpenAPI generator – remove any OAuth2PasswordBearer that sneaks in
# --------------------------------------------------------------------------- #
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # keep only our Bearer scheme
    comps = schema.setdefault("components", {})
    schemes = comps.setdefault("securitySchemes", {})
    schemes.pop("OAuth2PasswordBearer", None)  # ← ditch the username/password box

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi  # override FastAPI’s default generator


# --------------------------------------------------------------------------- #
#  Startup – make sure tables exist
# --------------------------------------------------------------------------- #
@app.on_event("startup")
async def startup_event():
    logger.info("Starting application…")
    await create_db_and_tables()
    logger.info("Database initialized")


# --------------------------------------------------------------------------- #
#  Routes
# --------------------------------------------------------------------------- #
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(wallets.router)

