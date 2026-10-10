# Public project backlog

Reviewed 10 October 2026. This file records status, not instructions to run scans.

## Integrated

- [x] Stable registry IDs and CPE / ACS / mixed / unknown service roles.
- [x] Added cwmp server and Telefónica cwmpWeb signatures.
- [x] A 93-query public catalog, including all 39 observation queries and research follow-ups.
- [x] Huawei authentication, country and auxiliary-port slices.
- [x] TR069 Client variants and related-family overlap caveats.
- [x] AVSystem version counts with a same-run denominator.
- [x] All 2,457 observed country–line operator slices in the October 10 full run.
- [x] Fresh timestamped snapshots, frozen resume plans and history index.
- [x] Automatic source-fact synchronization after a successful fresh full run.
- [x] Four-language interface and project news with source links.
- [x] Public English research editions and a research-to-atlas coverage inventory.

## Open research

- [ ] Establish the vendor and service role of cwmp server with independent evidence.
  Lanet's equipment catalog suggests candidates; none is a confirmed attribution.
- [ ] Resolve Gateway/TIM component attribution. Technicolor and ADB remain candidates.
- [ ] Identify the OEM carriers of the main TR069 Client component family.
- [ ] Validate any hardware-model interpretation of Huawei operator slices.
- [ ] Expand evaluation using a labeled holdout independent of discovery samples.
- [ ] Investigate transport-level signatures for obuspa without claiming absence.
- [ ] Review newly found versions before adding them to the query catalog.

## Publication scope

- [x] Passive and active fingerprinting results may be published; new vulnerability findings stay private.
- [x] Apache 2.0 for project-owned code and documentation.
- [x] The separately restricted `probes` package is excluded.
- [x] Public tree prepared without old research Git history.

Raw host records, firmware, credentials and operational research details are not
part of the public repository. Daily collection is supported but not scheduled.
