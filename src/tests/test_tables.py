# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Unit test cases for the table generator command line tool."""

from tables import __version__


def test_version():
    """Check teh version number is defined."""
    assert __version__ == "0.1.0"
