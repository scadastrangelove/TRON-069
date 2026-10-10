# Publication review — 10 October 2026

The public edition contains English research documents, dated Shodan aggregates,
the collector and builder, and two identical atlas entry points. Project-owned
code and documentation use Apache 2.0. `NOTICE` identifies third-party data sources.

## Included

- 52 lines with explicit service roles and source links.
- 2,457 country–line operator slices, 93 research queries and 39 observations.
- 31 research results mapped to atlas findings, news and documentation in
  [research-findings.json](../data/research-findings.json).
- Passive fingerprints and dated authorized active fingerprinting results.
- Historical aggregate measurements and their original timestamps.

## Excluded

New vulnerability findings and associated implementation/reproduction details,
the separate `probes` package, firmware/extracted binaries, raw host exports,
credentials, operational logs and the old research Git history. The research
originals are retained separately outside this public repository.

Public documents are edited English editions rather than unredacted translations.
Private annotations in historical collection plans are replaced by public prose;
`publication_redactions` records this. Measurement fields are unchanged.

## Validation

- Builder: 17 tests passed; collector: 28; fact synchronization: 6.
- Atlas source-function audit: 47 checks passed for each entry point, including
  language coverage, data consistency and source links from both path depths.
- All 3,148 saved aggregate responses were compared with research originals:
  query, count, time, facets and run metadata match.
- Manual document and embedded-data review, plus private-marker, raw-record and
  configured-key scans, found no excluded content in the reviewed public tree.
- Local browser checks covered news, observations, inspector evidence links,
  both entry-point paths, wrapping and console errors.
- Map provenance: all 177 country geometries match the cited Natural Earth source.

Run [the README checks](../README.md) after changes. Automated checks supplement
manual disclosure review; new text or data must be reviewed before publication.

## Fingerprint guidance follow-up

The public fingerprint guide now explains precedence of specific realms over
generic toolkit labels, while preserving all matches and independent query totals.
The gSOAP prose was aligned with its existing mixed service classification. No
probe-package files, new vulnerability findings or additional measurements were
added. The 52 lines, 93 queries and 39 collected observations are unchanged.

## Manifesto and pinned news

The English README now introduces the last-mile research mission, responsible
vendor collaboration and the Rust-in-Peace / Reproof tools. The manifesto is
translated into all four atlas languages and pinned above all dated news. A
future-dated test verifies that newer entries cannot displace it. The initial
ticker also opens with the manifesto. External project links use HTTPS; local
evidence points to the README manifesto anchor.
