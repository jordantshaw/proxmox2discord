
from fastapi import FastAPI, HTTPException

from .endpoints import router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Proxmox2Discord',
        description='Proxmox Discord notifier service',
    )

    app.include_router(router)

    return app


app = create_app()

