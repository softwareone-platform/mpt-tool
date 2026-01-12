import datetime as dt
from pathlib import Path

import typer

from mpt_tool.constants import MIGRATION_FOLDER
from mpt_tool.templates import MIGRATION_SCAFFOLDING_TEMPLATE

app = typer.Typer(help="MPT CLI - Migration tool for extensions.", no_args_is_help=True)


@app.callback()
def callback() -> None:
    """MPT CLI - Migration tool for extensions."""


@app.command("migrate")
def migrate(
    new_data: str | None = typer.Option(  # noqa: WPS404
        None,
        "--new-data",
        metavar="FILENAME",
        help="Scaffold a new data migration script with the provided filename.",
    ),
    new_schema: str | None = typer.Option(  # noqa: WPS404
        None,
        "--new-schema",
        metavar="FILENAME",
        help="Scaffold a new schema migration script with the provided filename.",
    ),
) -> None:
    """Migrate command."""
    if new_data and new_schema:
        raise typer.BadParameter(
            "Options --new-data and --new-schema cannot be combined.",
            param_hint="migrate",
        )

    if new_schema or new_data:
        filename_suffix = new_data or new_schema
        typer.echo(f"Scaffolding migration: {filename_suffix}.")
        migration_folder = Path(MIGRATION_FOLDER)
        migration_folder.mkdir(parents=True, exist_ok=True)
        timestamp = dt.datetime.now(tz=dt.UTC).strftime("%Y%m%d%H%M%S")
        # TODO: add filename validation
        filename = f"{timestamp}_{filename_suffix}.py"
        full_filename_path = migration_folder / filename
        try:
            full_filename_path.touch(exist_ok=False)
        except FileExistsError:
            typer.secho(f"File already exists: {filename}", fg=typer.colors.RED)
            raise typer.Abort

        full_filename_path.write_text(
            encoding="utf-8",
            data=MIGRATION_SCAFFOLDING_TEMPLATE.substitute(
                command_name="DataBaseCommand" if new_data else "SchemaBaseCommand"
            ),
        )
        typer.secho(f"Migration file: {filename} has been created.", fg=typer.colors.GREEN)
        return

    typer.secho("Running migrations is not implemented yet.", fg=typer.colors.YELLOW)


def main() -> None:
    """Entry point for the CLI."""
    app()
