from fastapi import FastAPI
from .routers import health,monitors
app=FastAPI(title="PingBoard",version="0.2.0")
app.include_router(health.router)
app.include_router(monitors.router)