from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Dict, Any
import uvicorn


# --- Database setup ---
DATABASE_URL = "sqlite:///./optiship-jaan.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Ship(Base):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


# --- Create tables ---
Base.metadata.create_all(bind=engine)


# --- FastAPI app ---
app = FastAPI(title="OptiShip‑Jaan MCP Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Dependency for database session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/mcp/health")
async def health():
    return {"status": "ok", "service": "mcp_server"}


@app.get("/mcp/admin/status")
async def admin_status():
    return {"status": "admin_dashboard_ready"}


# --- MCP Ship endpoints ---
@app.get("/mcp/admin/ships")
async def list_ships():
    db = SessionLocal()
    try:
        ships = db.query(Ship).all()
        return {
            "ships": [
                {
                    "id": ship.id,
                    "name": ship.name,
                    "type": ship.type,
                    "created_at": ship.created_at.isoformat(),
                }
                for ship in ships
            ]
        }
    finally:
        db.close()


@app.post("/mcp/admin/ships")
async def create_ship(payload: Dict[Any, Any]):
    db = SessionLocal()
    try:
        ship = Ship(
            name=payload.get("name", "Unnamed"),
            type=payload.get("type", "Unknown"),
        )
        db.add(ship)
        db.commit()
        db.refresh(ship)
        return {
            "status": "created",
            "ship": {
                "id": ship.id,
                "name": ship.name,
                "type": ship.type,
                "created_at": ship.created_at.isoformat(),
            },
        }
    finally:
        db.close()





