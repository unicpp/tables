# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Command Line Interface for the unicode tables generator."""

import click

from tables._version import __version__
from tables.ucd import eaw

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
def cli():
    """
    Parse source data from the Unicode Character Database and generate
    data tables for use in unic++.
    """


@cli.group("ucd")
def ucd_group():
    """
    Generate tables to implement access to character properties as defined in
    the Unicode® Standard Annex #44 - Unicode Character Database.
    """


@ucd_group.command("eaw")
@click.option(
    "--static/--no-static",
    default=True,
    help="declare the table as static or not",
)
@click.option(
    "--raw-array/--std-array",
    default=False,
    help="use a raw C array or C++ std::array",
)
@click.option(
    "-t",
    "--element-type",
    default="std::tuple<uint32_t, uint32_t, uint8_t, uint8_t>",
    help="the type of the elements in the array",
)
@click.option(
    "-n", "--name", default="unicode_eaw_table", help="the table variable name"
)
def eaw_command(static, raw_array, element_type, name):
    """
    Generate tables from the EastAsianWidth.txt source file.

    For more information, see UAX #11: East Asian Width, at
    https://www.unicode.org/reports/tr11/
    """

    eaw.run(
        static=static,
        raw_array=raw_array,
        element_type=element_type,
        qualified_name=name,
    )


def main():
    """Invoke the command line interface main entry point."""
    cli()
