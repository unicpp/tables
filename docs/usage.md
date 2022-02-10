# Usage

## UNicode character width table

```shell
Usage: tables ucd eaw [OPTIONS]

  Generate tables from the EastAsianWidth.txt source file.

  For more information, see UAX #11: East Asian Width, at
  https://www.unicode.org/reports/tr11/

Options:
  --static / --no-static     declare the table as static or not
  --raw-array / --std-array  use a raw C array or C++ std::array
  -t, --element-type TEXT    the type of the elements in the array
  -n, --name TEXT            the table variable name
  -h, --help                 Show this message and exit.
```

A typical usage is as following:

```shell
tables ucd eaw > unicode_width.incl
```

Then in the C++ file, where the table is needed, simply include the file:

```cpp
#include "unicode_width.incl"
```
