# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Configuration for python setuptools."""

from setuptools import setup

setup(
    setup_requires=["pbr"],
    pbr=True,
)
