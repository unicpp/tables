# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Table generator for the Unicode East Asian Character Width data."""

from tables.ucd import categories, east_asian_width


def emit_table(
    table,
    version,
    static=False,
    raw_array=False,
    element_type="std::tuple<uint32_t, uint32_t, uint8_t, uint8_t>",
    qualified_name="unicode_eaw_table",
):
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    """
    Generate the table containing code points and their recommended character
    width for CJK and non-CJK contexts.
    """
    print(
        "// This table was generated from Unicode Character Database version "
        + f"{version}"
    )
    print(f"// https://www.unicode.org/Public/{version}/")
    static_qualifier = "static " if static else ""
    var_type = (
        element_type
        if raw_array
        else f"std::array<{element_type}, {len(table)}>"
    )
    variable = f"{qualified_name}{'[]' if raw_array else ''}"
    decl = f"const {var_type} {variable}"
    print(f"{static_qualifier}{decl} = {'{' if raw_array else '{{'}")
    data = ""
    first = True
    new_line = 4
    for interval in table:
        if not first:
            data += ", "
        if new_line == 0:
            data += "\n"
            new_line = 4
        first = False
        [low, high, width, cjk_width] = interval
        data += "{" + f"0x{high:X}, 0x{low:X}, {width}, {cjk_width}" + "}"
        new_line -= 1
    print(data)
    print(f"{'}' if raw_array else '}}'};\n")


def run(static, raw_array, element_type, qualified_name):
    """Run the command line command using the passed arguments."""

    version = "14.0.0"

    gencats = categories.load(version)

    width_table = []
    for zwcat in ["Me", "Mn", "Cf"]:
        width_table.extend(
            [
                (lo_hi[0], lo_hi[1], 0, 0)
                for lo_hi in gencats[zwcat]
                # SOFT HYPHEN (U+00AD) has a column width of 1.
                # it is on a separate line as a single value in the database
                if not (lo_hi[0] == 0xAD and lo_hi[1] == 0xAD)
            ]
        )
    # 1160..11FF;N
    # Lo   [160] HANGUL JUNGSEONG FILLER..HANGUL JONGSEONG SSANGNIEUN
    width_table.append((0x1160, 0x11FF, 0, 0))

    # get the rest of the widths, except those that are explicitly marked
    # zero-width above from the EastAsianWidth.txt database
    ea_widths = east_asian_width.load(
        version, ["W", "F", "A"], ["Me", "Mn", "Cf"]
    )

    # These always map to fullwidth (2) characters.
    for dwcat in ["W", "F"]:
        width_table.extend(
            [(lo_hi1[0], lo_hi1[1], 2, 2) for lo_hi1 in ea_widths[dwcat]]
        )

    # Ambiguous Unicode characters always map to fullwidth (2) characters when
    # mapping Unicode to East Asian legacy character encodings, and to regular
    # (1) characters otherwise.
    width_table.extend(
        [(lo_hi2[0], lo_hi2[1], 1, 2) for lo_hi2 in ea_widths["A"]]
    )

    width_table.sort(key=lambda w: w[0])

    print(len(width_table))

    width_table = east_asian_width.optimize(width_table)

    print(len(width_table))

    emit_table(
        width_table,
        version,
        static=static,
        raw_array=raw_array,
        element_type=element_type,
        qualified_name=qualified_name,
    )
