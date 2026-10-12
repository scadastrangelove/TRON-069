# Public project backlog

Reviewed 13 October 2026. This file records status, not instructions to run scans.

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
- [x] Identify the software family of the main TR069 Client component: binary-proven as Works Systems OneAgent TR (October 13). Device OEM carriers are not derivable from the response and remain unlabeled.
- [x] Close RAC2V1K, F609/F612 and Arcadyan BRN acquisition hunts for component attribution; retain bounded results in the dossier.
- [ ] Verify the EZpacket Agent4.0 distribution link with a response template or binary; object-name similarity remains a hypothesis.
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

## Fingerprint follow-up

- [x] Add F670L second-image evidence and Huawei port-30005 firmware evidence to line cards, sources and four-language news.
- [x] Align the TR069 Client component-lineage badge and publish the sub-family fingerprint guide without a separate population count.
- [x] Publish the USP transport fingerprint note; distinguish protocol identification from obuspa implementation attribution.
- [ ] Test candidate vendor attributions for cwmp server against public firmware and source evidence.
- [ ] Complete the public nonce-format census for ZTE and TP-Link client families.
  The newer ZTE F670L platform is covered by firmware analysis (October 12);
  the open part is the older inspected generation's binary, which would show
  whether the visible `cpe@zte.com` fleet shares that nonce format.
- [ ] Check a WAN-exposed F670L banner (port 58000) for the opaque stub to
  decide whether the ZTE matcher should split by generation.
- [ ] Expand the passive IgdAuth sample and compare the marker format with SDK sources.
- [ ] Validate USP transport markers across implementations and preserve dated query responses before adding a counted USP line.

## ACS research and atlas integration

- [x] Separate relationship evidence from count observations.
- [x] Add the CPE–ACS graph with evidence filters, source cards and map links.
- [x] Add the measured country–operator–signature network, flow overview and matrix, exact aliases and corporate grouping.
- [x] Keep the network on mobile; support neighbor expansion, node pinning, pan, pinch zoom and shared neighborhoods.
- [ ] Refresh truncated organization facets in new dated snapshots; retain joint scope for future ASN/port drills.
- [x] Publish an English integration matrix and firmware-configuration summary.
- [x] Add the general Bad CPE trust-boundary model and four-language news.
- [ ] Record image hashes and redacted configuration excerpts for firmware-derived endpoints.
- [ ] Resolve Gateway/TIM component attribution and nld-acs.com ownership independently.
- [ ] Find named operator deployments for RDK-B and GenieACS.
- [ ] Add exact public sources for the BT community-log lead.
- [ ] Extend the relationship catalog when operator, model and version evidence can be matched.
