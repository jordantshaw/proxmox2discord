import uvicorn
import typer

from pathlib import Path
from typing import Optional


app = typer.Typer(help="Manage and run the proxmox2discord web server.")


@app.command()
def serve(
    host: str = typer.Option(
        "127.0.0.1", "--host", "-h", help="Host/IP to bind the server on."
    ),
    port: int = typer.Option(
        6068, "--port", "-p", help="Port to listen on."
    ),
    log_level: str = typer.Option(
        "info", "--log-level", "-l", help="Uvicorn log level."
    ),
    uvicorn_config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Path to a Uvicorn config file (Python).",
    ),
):
    """ Start proxmox2discord web server. """

    if uvicorn_config:
        import subprocess
        subprocess.run(["uvicorn", "--config", str(uvicorn_config)])
        raise typer.Exit()

    uvicorn.run(
        "proxmox2discord.main:app",
        host=host,
        port=port,
        log_level=log_level,
    )


if __name__ == "__main__":
    app()