"""CLI entry point"""

import typer
from rich.console import Console

from ivryaa.dialog.session import DialogSession
from ivryaa.utils.logger import logger

app = typer.Typer(help="IVRyaa - Check server metrics via voice")
console = Console()


@app.command()
def start() -> None:
    """Start a voice dialog session"""
    logger.info("Starting IVRyaa...")

    try:
        session = DialogSession()
        session.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Ending session[/yellow]")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """Display current system metrics (without voice)"""
    from ivryaa.metrics import get_all_metrics

    metrics = get_all_metrics()
    console.print("[bold]System Metrics[/bold]")
    console.print(f"  CPU Usage: {metrics['cpu']:.1f}%")
    console.print(f"  Memory Usage: {metrics['memory']:.1f}%")
    console.print(f"  Disk Usage: {metrics['disk']:.1f}%")


@app.command()
def version() -> None:
    """Display version"""
    from ivryaa import __version__

    console.print(f"IVRyaa v{__version__}")


if __name__ == "__main__":
    app()
