from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.middleware import InMemoryRateLimitMiddleware, RequestContextMiddleware, SecurityHeadersMiddleware


def create_app() -> FastAPI:
    settings.validate_production_security()
    app = FastAPI(
        title="Cyber Risk Radar API",
        version="0.1.0",
        description="Continuous cyber risk monitoring and security posture assessment for SMEs.",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(InMemoryRateLimitMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()
