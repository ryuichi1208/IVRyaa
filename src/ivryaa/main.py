"""CLIエントリーポイント"""

import typer
from rich.console import Console

from ivryaa.dialog.session import DialogSession
from ivryaa.utils.logger import logger

app = typer.Typer(help="IVRyaa - 音声でサーバーメトリクスを確認")
console = Console()


@app.command()
def start() -> None:
    """音声対話セッションを開始する"""
    logger.info("IVRyaaを起動しています...")

    try:
        session = DialogSession()
        session.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]セッションを終了します[/yellow]")
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """現在のシステムメトリクスを表示する（音声なし）"""
    from ivryaa.metrics import get_all_metrics

    metrics = get_all_metrics()
    console.print("[bold]システムメトリクス[/bold]")
    console.print(f"  CPU使用率: {metrics['cpu']:.1f}%")
    console.print(f"  メモリ使用率: {metrics['memory']:.1f}%")
    console.print(f"  ディスク使用率: {metrics['disk']:.1f}%")


@app.command()
def version() -> None:
    """バージョンを表示する"""
    from ivryaa import __version__

    console.print(f"IVRyaa v{__version__}")


if __name__ == "__main__":
    app()
