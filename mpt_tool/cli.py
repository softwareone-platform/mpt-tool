import typer

app = typer.Typer(help="MPT CLI - Migration tool for extensions.", no_args_is_help=True)


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
