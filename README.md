# Provider parser

Script that calls staging Tink API to retrieve provider conditions for lsit of providers.

## Input:
`BEARER_TOKEN` - overrite the client token for tink api there.
`providers.json` - providers for which data will be collected.

## Output:
`out.csv` - Excell friendly output file. Mind that `;` is the separator.
Column order is set in the `RULES_DICT` in the python file.
