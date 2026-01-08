from pathlib import Path

import typer

app = typer.Typer(help="MPT CLI - Migration tool for extensions.", no_args_is_help=True)


@app.command()
def init() -> None:
    """Initialize the migrations tool workspace."""
    root = Path.cwd()

    settings_file = root / "settings.py"
    if not settings_file.exists():
        typer.secho("Settings file does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    migrations_dir = root / "migrations"
    if migrations_dir.exists():
        typer.secho("Migrations folder already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    migrations_dir.mkdir(exist_ok=True)

    init_file = migrations_dir / "__init__.py"
    init_file.touch(exist_ok=True)

    state_file = root / ".migrations-state.json"
    if state_file.exists():
        typer.secho("State file already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not state_file.exists():
        state_file.write_text("{}\n")


@app.callback()
def callback() -> None:
    """MPT CLI - Migration tool for extensions."""


@app.command()
def migrate() -> None:
    """Run the migration process."""
    typer.echo("Hello World!")


def main() -> None:
    """Entry point for the CLI."""
    app()
