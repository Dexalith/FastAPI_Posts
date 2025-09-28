import uvicorn
from fastapi import FastAPI

from app.api.news_api import router as api_router
from app.api.auth_api import router as auth_router
from app.configuration_db.conf import app_config


def create_application() -> FastAPI:
    app_instance = FastAPI(
        title=app_config.project_name,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
    )

    app_instance.include_router(api_router)
    app_instance.include_router(auth_router)

    return app_instance

app = create_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_config.app_host,
        port=app_config.app_port,
        reload=True,
    )