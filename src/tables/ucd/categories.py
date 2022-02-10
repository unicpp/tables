# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Load and process data from Unicode Character Data database (UnicodeData)."""

import requests

from tables.ucd import utils

# Mapping taken from Table 12 from:
# http://www.unicode.org/reports/tr44/#General_Category_Values
expanded_categories = {
    "Lu": ["LC", "L"],
    "Ll": ["LC", "L"],
    "Lt": ["LC", "L"],
    "Lm": ["L"],
    "Lo": ["L"],
    "Mn": ["M"],
    "Mc": ["M"],
    "Me": ["M"],
    "Nd": ["N"],
    "Nl": ["N"],
    "No": ["No"],
    "Pc": ["P"],
    "Pd": ["P"],
    "Ps": ["P"],
    "Pe": ["P"],
    "Pi": ["P"],
    "Pf": ["P"],
    "Po": ["P"],
    "Sm": ["S"],
    "Sc": ["S"],
    "Sk": ["S"],
    "So": ["S"],
    "Zs": ["Z"],
    "Zl": ["Z"],
    "Zp": ["Z"],
    "Cc": ["C"],
    "Cf": ["C"],
    "Cs": ["C"],
    "Co": ["C"],
    "Cn": ["C"],
}

# Isolated surrogate code points have no interpretation; consequently, no
# character code charts or names lists are provided for this range.
surrogate_codepoints = (0xD800, 0xDFFF)


def _is_surrogate(code_point):
    return surrogate_codepoints[0] <= code_point <= surrogate_codepoints[1]


def _tidy_cats(cats):
    cats_out = {}
    for cat in cats:
        cats_out[cat] = _tidy_cat(cats[cat])
    return cats_out


def _tidy_cat(cat):
    cat_out = []
    letters = sorted(set(cat))
    cur_start = letters.pop(0)
    cur_end = cur_start
    for letter in letters:
        assert (
            letter > cur_end
        ), f"cur_end: {hex(cur_end)}, letter: {hex(letter)}"
        if letter == cur_end + 1:
            cur_end = letter
        else:
            cat_out.append((cur_start, cur_end))
            cur_start = cur_end = letter
    cat_out.append((cur_start, cur_end))
    return cat_out


def load(version):
    """
    Load and process teh data from  Unicode Character Data database
    (UnicodeData).

    Args:
        version (string): unicode standard version number

    Raises:
        SystemExit: if an exception occurs while fetching the data

    Returns:
        dictionary: the key is a unicode general category
        (https://www.unicode.org/reports/tr44/#General_Category_Values) and the
        value is the list of code point intervals for that category. Each
        interval is a tuple (low, high).
    """

    source_url = f"https://www.unicode.org/Public/{version}/ucd/UnicodeData.txt"

    print("Parsing categories from source: " + source_url)
    try:
        [response, block_size, progress_bar] = utils.start_request(source_url)

        cats = {}
        udict = {}
        range_start = -1
        for line in response.iter_lines(block_size, decode_unicode=True):
            progress_bar.update(len(line) + 1)
            if line.startswith("#"):
                continue
            data = line.split(";")
            assert len(data) == 15, (
                "unexpected downloaded data format, "
                + f"expecting a line with 15 fields, got {len(data)}, ({data})"
            )
            assert (
                data[2] in expanded_categories
            ), f"unknown general category '{data[2]}' in line '{line}'"
            code_point = int(data[0], 16)
            if _is_surrogate(code_point):
                continue
            if range_start >= 0:
                for i in range(range_start, code_point):
                    udict[i] = data
                range_start = -1
            if data[1].endswith(", First>"):
                range_start = code_point
                continue
            udict[code_point] = data

        progress_bar.close()

        for code_point, data in udict.items():
            gencat = data[2]
            if gencat not in cats:
                cats[gencat] = []
            cats[gencat].append(code_point)

        cats = _tidy_cats(cats)

        return cats

    except requests.exceptions.RequestException as err:
        raise SystemExit from err
