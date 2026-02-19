import logging
from typing import Annotated

import typer

from mpt_tool.commands import CommandFactory, MigrateCommandValidator
from mpt_tool.commands.errors import BadParameterError, CommandNotFoundError
from mpt_tool.use_cases.errors import UseCaseError

app = typer.Typer(help="MPT CLI - Migration tool for extensions.", no_args_is_help=True)


@app.callback()
def callback() -> None:
    """MPT CLI - Migration tool for extensions."""


@app.command("migrate")
def migrate(  # noqa: WPS211
    ctx: typer.Context,
    check: Annotated[  # noqa: FBT002
        bool, typer.Option("--check", help="Check for duplicate migration_id in migrations.")
    ] = False,
    data: Annotated[bool, typer.Option("--data", help="Run data migrations.")] = False,  # noqa: FBT002
    schema: Annotated[bool, typer.Option("--schema", help="Run schema migrations.")] = False,  # noqa: FBT002
    manual: Annotated[
        str | None,
        typer.Option(
            "--manual",
            help="Mark the migration provided as applied without running it",
            metavar="MIGRATION_ID",
        ),
    ] = None,
    init: Annotated[  # noqa: FBT002
        bool, typer.Option("--init", help="Initialize migration tool resources.")
    ] = False,
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
    list: Annotated[bool, typer.Option("--list", help="List all migrations.")] = False,  # noqa: A002, FBT002
    migration_id: Annotated[
        str | None, typer.Argument(help="Optional migration ID for --data or --schema.")
    ] = None,
) -> None:
    """Migrate command."""
    try:
        MigrateCommandValidator.validate(ctx.params)
    except BadParameterError as error:
        raise typer.BadParameter(str(error), param_hint="migrate")

    try:
        command_instance = CommandFactory.get_instance(ctx.params)
    except CommandNotFoundError:
        raise typer.BadParameter("No valid param provided.", param_hint="migrate")

    typer.echo(command_instance.start_message)
    try:
        command_instance.run()
    except UseCaseError as error:
        typer.secho(
            f"Error running {command_instance.name} command: {error!s}",
            fg=typer.colors.RED,
        )
        raise typer.Abort

    typer.secho(command_instance.success_message, fg=typer.colors.GREEN)


def main() -> None:
    """Entry point for the CLI."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    app()
