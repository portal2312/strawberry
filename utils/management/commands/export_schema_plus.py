"""Override strawberry-django export_schema."""

import functools
import pathlib

from django.core.management.base import CommandError
from django.utils import autoreload
from strawberry import Schema
from strawberry.printer import print_schema
from strawberry.utils.importer import import_module_symbol
from strawberry_django.management.commands.export_schema import Command as BaseCommand


class Command(BaseCommand):
    """Override strawberry-django export_schema Command class."""

    help = "Export the graphql schema"

    def add_arguments(self, parser):
        """Override."""
        super().add_arguments(parser)
        parser.add_argument(
            "--watch",
            dest="watch",
            default=False,
            action="store_true",
            help="Updates the schema on file changes (default: False)",
        )

    def handle(self, *args, **options):
        """Overwrite."""
        try:
            schema_symbol = import_module_symbol(
                options["schema"][0],
                default_symbol_name="schema",
            )
        except (ImportError, AttributeError) as e:
            raise CommandError(str(e)) from e

        if not isinstance(schema_symbol, Schema):
            raise CommandError("The `schema` must be an instance of strawberry.Schema")

        schema_output = print_schema(schema_symbol)
        path = options.get("path")
        watch = options.get("watch")
        if path:
            if watch:
                autoreload.run_with_reloader(
                    functools.partial(pathlib.Path(path).write_text, schema_output)
                )
            else:
                pathlib.Path(path).write_text(schema_output)
        else:
            if watch:
                autoreload.run_with_reloader(
                    functools.partial(self.stdout.write, schema_output)
                )
            else:
                self.stdout.write(schema_output)
