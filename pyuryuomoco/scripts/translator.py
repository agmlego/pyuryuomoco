# pylint: disable=logging-fstring-interpolation

import logging

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from ..cluster import *
from ..substitution import *

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
log = logging.getLogger(__name__)


@click.group(invoke_without_command=True)
@click.version_option()
@click.option(
    "--cluster/--no-cluster",
    type=bool,
    default=True,
    help="Whether to apply clustering rules",
)
@click.option(
    "--check-dict/--no-check-dict",
    type=bool,
    default=True,
    help="Whether to check for non-English words prior to output",
)
@click.pass_context
def cli(ctx: click.Context, cluster: bool, check_dict: bool):
    ctx.ensure_object(dict)
    ctx.obj["CLUSTER"] = cluster
    ctx.obj["CHECK_DICT"] = check_dict


@cli.command()
@click.argument("phrases", nargs=-1, type=str)
@click.pass_context
def english(ctx: click.Context, phrases: str):
    """Translate English PHRASE(s) to Uryuomoco"""
    log.debug(f"English to Uryuomoco:")
    table = Table(title="English to Uryuomoco")
    table.add_column("English", style="cyan")
    table.add_column("Uryuomoco", style="green")

    for phrase in phrases:
        if ctx.obj["CLUSTER"]:
            sub = cluster_english(phrase=phrase)
        else:
            sub = substitute_english(phrase=phrase)
        table.add_row(phrase, sub)

    console = Console()
    console.print(table)


@cli.command()
@click.argument("phrases", nargs=-1, type=str)
@click.pass_context
def uryuomoco(ctx: click.Context, phrases: str):
    """Translate Uryuomoco PHRASE(s) to English"""
    log.debug(f"Uryuomoco to English")
    table = Table(title="Uryuomoco to English")
    table.add_column("Uryuomoco", style="green")
    table.add_column("English", style="cyan")

    for phrase in phrases:
        if ctx.obj["CLUSTER"]:
            sub = cluster_uryuomoco(phrase=phrase)
        else:
            sub = substitute_uryuomoco(phrase=phrase)
        table.add_row(phrase, sub)

    console = Console()
    console.print(table)
