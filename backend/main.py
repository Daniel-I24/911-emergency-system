from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.patient_routes import router as patient_router
from backend.routes.ui_routes import router as ui_router


APP_TITLE = "Hospital Queue API"
ALLOW_ALL_ORIGINS: list[str] = ["*"]
ALLOW_ALL_METHODS: list[str] = ["*"]
ALLOW_ALL_HEADERS: list[str] = ["*"]


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=APP_TITLE)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ALL_ORIGINS,
        allow_credentials=False,
        allow_methods=ALLOW_ALL_METHODS,
        allow_headers=ALLOW_ALL_HEADERS,
    )

    app.include_router(ui_router)
    app.include_router(patient_router)
    return app


app = create_app()
