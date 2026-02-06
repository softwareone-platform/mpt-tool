from typing import override

from mpt_tool.commands.base import BaseCommand
from mpt_tool.use_cases import InitializeUseCase


class InitCommand(BaseCommand):
    """Initialize migration tool resources."""

    @override
    @property
    def start_message(self) -> str:
        return "Initializing migration tool..."

    @override
    @property
    def success_message(self) -> str:
        return "Migration tool initialized successfully."

    @override
    def run(self) -> None:
        InitializeUseCase().execute()
