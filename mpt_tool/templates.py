from string import Template

MIGRATION_SCAFFOLDING_FILE_TEXT = """\
from mpt_tool.commands import $command_name


class Command($command_name):
    def run(self):
        # implement your logic here
        pass
"""
MIGRATION_SCAFFOLDING_TEMPLATE: Template = Template(MIGRATION_SCAFFOLDING_FILE_TEXT)
