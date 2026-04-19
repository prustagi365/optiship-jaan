from fastapi import FastAPI
from fastapi_admin import AdminDashboard, create_app
from fastapi_admin.providers import BasicAdminAuthProvider

from src.mcp_server.models import Base, engine, SessionLocal, Ship


async def setup_admin():
    app = FastAPI(title="OptiShip‑Jaan Admin Dashboard")

    auth_provider = BasicAdminAuthProvider(
        username="admin",
        password="admin_password_here",  # change this in prod
    )

    admin = AdminDashboard(
        app=app,
        auth_provider=auth_provider,
        prefix="/admin",
        secret_key="a_very_long_secret_key_here_min_32_chars",
    )

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Register the Ship model with the admin if your FastAPI‑admin variant supports it
    # (exact syntax may vary by version; this is a sketch)
    # admin.register_model(Ship)

    # Apply admin routes
    await admin.init()
    return app
