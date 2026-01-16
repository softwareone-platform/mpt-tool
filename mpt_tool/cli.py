import logging
from typing import Annotated, cast

import typer

from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.errors import NewMigrationError, RunMigrationError
from mpt_tool.use_cases import RunMigrationsUseCase
from mpt_tool.use_cases.new_migration import NewMigrationUseCase

app = typer.Typer(help="MPT CLI - Migration tool for extensions.", no_args_is_help=True)


@app.callback()
def callback() -> None:
    """MPT CLI - Migration tool for extensions."""


@app.command("migrate")
def migrate(  # noqa: C901, WPS238, WPS231
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
        migration_type = MigrationTypeEnum.DATA if new_data else MigrationTypeEnum.SCHEMA
        typer.echo(f"Scaffolding migration: {filename_suffix}.")
        try:
            filename = NewMigrationUseCase().execute(migration_type, cast(str, filename_suffix))
        except NewMigrationError as error:
            typer.secho(f"Error creating migration: {error!s}", fg=typer.colors.RED)
            raise typer.Abort

        typer.secho(f"Migration file: {filename} has been created.", fg=typer.colors.GREEN)


def main() -> None:
    """Entry point for the CLI."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    app()
