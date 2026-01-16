import datetime as dt
import logging
from pathlib import Path
from typing import Annotated

import typer

from mpt_tool.constants import MIGRATION_FOLDER
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.errors import RunMigrationError
from mpt_tool.templates import MIGRATION_SCAFFOLDING_TEMPLATE
from mpt_tool.use_cases import RunMigrationsUseCase

app = typer.Typer(help="MPT CLI - Migration tool for extensions.", no_args_is_help=True)


@app.callback()
def callback() -> None:
    """MPT CLI - Migration tool for extensions."""


@app.command("migrate")
def migrate(  # noqa: C901, WPS238, WPS210, WPS213, WPS231
    data: Annotated[bool, typer.Option("--data", help="Run data migrations.")] = False,  # noqa: FBT002
    schema: Annotated[bool, typer.Option("--schema", help="Run schema migrations.")] = False,  # noqa: FBT002
    new_data: Annotated[
        str | None,
        typer.Option(
            "--new-data",
            metavar="FILENAME",
            help="Scaffold a new data migration script with the provided filename.",
        ),
    ] = None,
    new_schema: Annotated[
        str | None,
        typer.Option(
            "--new-schema",
            metavar="FILENAME",
            help="Scaffold a new schema migration script with the provided filename.",
        ),
    ] = None,
) -> None:
    """Migrate command."""
    options = sum([bool(data), bool(schema), bool(new_data), bool(new_schema)])  # noqa: WPS221
    if options > 1:
        raise typer.BadParameter("Only one option can be used.", param_hint="migrate")
    if not options:
        raise typer.BadParameter("At least one option must be used.", param_hint="migrate")

    if data or schema:
        migration_type = MigrationTypeEnum.DATA if data else MigrationTypeEnum.SCHEMA
        typer.echo(f"Running {migration_type} migrations...")

        run_migration = RunMigrationsUseCase()
        try:
            run_migration.execute(migration_type)
        except RunMigrationError as error:
            typer.secho(f"Error running migrations: {error!s}", fg=typer.colors.RED)
            raise typer.Abort

        typer.secho("Migrations completed successfully.", fg=typer.colors.GREEN)
        return

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


def main() -> None:
    """Entry point for the CLI."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    app()
