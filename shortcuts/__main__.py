#!/usr/bin/env python3

import click

from . import Config, create_shortcuts


@click.group()
def cli() -> None:
    """
    Creates shortcut shell scripts from a configuration file.
    See https://github.com/seanbreckenridge/shortcuts for more information
    """


@cli.command(name="create")
@click.option("--debug/--quiet", default=False, help="Log shortcut files being created")
@click.option(
    "--conf",
    envvar="SHORTCUTS_CONFIG",
    type=click.Path(exists=True),
    default=str(Config.config_file),
    help="specify a configuration file",
)
@click.option(
    "--shortcuts-dir",
    envvar="SHORTCUTS_DIR",
    type=click.Path(),
    default=str(Config.shortcuts_dir),
    help="specify a shortcuts directory",
)
def create(debug: bool, conf: str, shortcuts_dir: str) -> None:
    """
    Create the shell scripts!
    """
    create_shortcuts(debug, conf, shortcuts_dir)


if __name__ == "__main__":
    cli(prog_name="shortcuts")
