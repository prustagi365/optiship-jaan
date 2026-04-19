from src.mcp_server.main import app
from src.admin_dashboard import setup_admin


# Mount the admin dashboard
import asyncio
admin_app = asyncio.run(setup_admin())
app.mount("/admin", admin_app, name="admin_dashboard")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
