# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Unicode East Asian Width data loading and processing."""

# Implementation inspired by https://github.com/unicode-rs/unicode-width and
# https://www.cl.cam.ac.uk/~mgk25/ucs/wcwidth.c

import re

import requests

from tables.ucd import utils


# pylint: disable-next=too-many-locals
def load(version, want_widths, except_cats):
    """
    Load the data from the Unicode Character Database and process it for
    in-memory format.

    Args:
        version (string): unicode version want_widths (list of strings):
        possible values are
            "A" : Ambiguous, "F" : Fullwidth, "H" : Halfwidth, "N" : Narrow,
            "Na" : Neutral (= Not East Asian), "W" : Wide
        except_cats (list of string): categories to be excluded from the result
        (see categories.expanded_categories for a list of acceptable values)

    Raises:
        SystemExit: if an exception occurs while loading the data

    Returns:
        list of intervals: each interval is a tuple (low, high)
    """
    source_url = (
        f"https://www.unicode.org/Public/{version}/ucd/EastAsianWidth.txt"
    )

    print("Parsing widths from source: " + source_url)
    try:
        [response, block_size, progress_bar] = utils.start_request(source_url)

        widths = {}
        re1 = re.compile(r"^([0-9A-F]+);(\w+) +# (\w+)")
        re2 = re.compile(r"^([0-9A-F]+)\.\.([0-9A-F]+);(\w+) +# (\w+)")
        for line in response.iter_lines(block_size, decode_unicode=True):
            progress_bar.update(len(line) + 1)
            if line.startswith("#"):
                continue
            width = None
            d_lo = 0
            d_hi = 0
            cat = None
            matches = re1.match(line)
            if matches:
                d_lo = matches.group(1)
                d_hi = matches.group(1)
                width = matches.group(2)
                cat = matches.group(3)
            else:
                matches = re2.match(line)
                if matches:
                    d_lo = matches.group(1)
                    d_hi = matches.group(2)
                    width = matches.group(3)
                    cat = matches.group(4)
                else:
                    continue
            if cat in except_cats or width not in want_widths:
                continue
            d_lo = int(d_lo, 16)
            d_hi = int(d_hi, 16)
            if width not in widths:
                widths[width] = []
            widths[width].append((d_lo, d_hi))

        progress_bar.close()

        return widths

    except requests.exceptions.RequestException as err:
        raise SystemExit from err


def optimize(wtable):
    """
    Optimize the table by collapsing adjacent intervals when possible.

    Args:
        wtable (list): the widths table

    Returns:
        [type]: [description]
    """
    wtable_out = []
    w_this = wtable.pop(0)
    while wtable:
        if w_this[1] == wtable[0][0] - 1 and w_this[2:3] == wtable[0][2:3]:
            w_tmp = wtable.pop(0)
            w_this = (w_this[0], w_tmp[1], w_tmp[2], w_tmp[3])
        else:
            wtable_out.append(w_this)
            w_this = wtable.pop(0)
    wtable_out.append(w_this)
    return wtable_out
