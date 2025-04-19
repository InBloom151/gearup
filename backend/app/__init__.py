from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import router as api_router

def create_app(*, lifespan=None) -> FastAPI:
    app = FastAPI(
        title="GearUp API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # ───── Middlewares (CORS, logging, etc.) ─────
    origins = ["http://localhost:5173"]  # TODO future frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ───── Routers ─────────
    app.include_router(api_router, prefix="/api/v1")

    # ───── Health check ─────
    @app.get("/health", include_in_schema=False)
    async def _health() -> dict[str, str]:
        return {"status": "ok"}

    return app