# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Unit test cases for the table generator command line tool."""

import re

from tables import __version__


def test_version():
    """Check teh version number is defined."""
    version_regexp = re.compile(r"^\d+(\.\d+){2}")
    assert version_regexp.match(__version__)
