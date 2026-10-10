# Atlas correctness fixes

Public summary, 10 October 2026.

Operator filtering now uses the actual collected facets and reports their finite coverage. It does not impute uncollected tails. Line and country exports follow the same slice logic as the interface. Region and country selections intersect. Missing observations display no current count. Dedicated ACS lines are labeled and excluded from the default CPE-oriented sum. Historical query overlap remains a method limitation.

Run the current offline test commands in [README.md](../README.md) for reproducible validation.
