# TRON-069

**by SCADA StrangeLove** · A Global TR-069 Atlas

**[Explore the live atlas](https://scadastrangelove.github.io/TRON-069/)**

<a id="manifesto"></a>
## The last mile matters

TRON-069 exists to draw attention to the (in)security of the last mile: the
familiar little boxes that connect our homes to the Internet. Routers and modems
rarely command the attention given to wind turbines or power-generation control
systems. Yet they are part of the Internet's invisible foundation. A healthy
backbone is not enough: when the last mile fails, access disappears.

Continuing the tradition of SCADA StrangeLove, SCADA SOS and SD-WAN New Hop, we
make overlooked infrastructure visible and work responsibly with vendors to
investigate vulnerabilities, coordinate disclosure and verify fixes. We want
research to lead to safer devices and a more dependable Internet, making the
world a little better for the people who rely on it.

Our research uses agentic technologies, including
[Rust-in-Peace](https://github.com/scadastrangelove/rust-in-peace) and
[Reproof](https://github.com/scadastrangelove/reproof), to support investigation,
reproduction and verification. Evidence, human review and responsible disclosure
guide what we publish.

## Explore the atlas

An interactive atlas of TR-069/CWMP signatures, countries and network operators,
built from dated Shodan aggregates. Explore the map, compare implementations,
inspect operator slices and follow each research observation to its source.
The interface supports English, Spanish, Chinese and Russian.

News includes project updates and public research about the fleet. Selecting a
component, operator or country shows the three latest linked stories in the
map inspector. Open a story without losing the map filters, language or collection date;
its URL can be shared directly. The news page has Project, Fleet and Related
filters. News remains current when viewing historical measurements.

Edit `data/project-news.json` to add stories. Supply `title` and `body` in all four
languages, a publication date, and primary-source `links` for `kind: "fleet"`.
Optional `related.lines` uses registry IDs, `related.operators` uses IDs from
`data/operator-catalog.json`, and `related.countries` uses two-letter country
codes. Relationships are editorial context, not vulnerability counts. Matching
uses any explicitly linked selected entity and shows the reason; it does not
infer vulnerability from a shared country, vendor or HTTP banner. Operator
aliases are exact and country-scoped. `important: true` highlights a story;
the manifesto remains first in the full feed.

**Current collection: 29 October 2026.** 55 signature lines,
2,797 country–line operator slices, 131 research queries and
48 additional observations. Full collection ran from 20:09:25 to
21:05:33 UTC; individual results retain their own timestamps.
RomPager and mini_httpd cover all ports. [Cloud-network cohorts](LEGACY-HTTP.md#honeypots)
make suspected honeypot contamination visible alongside the raw component counts.
These are search matches, not a census of unique devices or vulnerable systems.

## Bring Your Own TR-069

**We have the banners. You may have the firmware.**

Help identify the implementations behind unresolved TR-069 signatures.
The [wanted list](WANTED.md) names the missing evidence for each search;
it is also available in the [atlas](https://scadastrangelove.github.io/TRON-069/#lang=en&tab=wanted).
Use **I have this** to open a prefilled GitHub issue with a public firmware or
GPL link, known model/version details and a sanitized fingerprint. New signatures
and attribution corrections are welcome too.

Public issues accept links and sanitized evidence. Do not attach firmware,
raw dumps, configurations, credentials or unpublished vulnerability details.
For non-public material, arrange a private transfer with a maintainer first.
Confirmed results receive an atlas source, a news entry and credit as requested.

## Open the atlas

`index.html` is the public entry point. `atlas/tr-atlas.html` is an identical copy.
Both include their data and map geometry, so the interactive atlas works offline.
Source-document links require the accompanying repository files.

```bash
python3 -m http.server 8766 --bind 127.0.0.1
# Open http://127.0.0.1:8766/index.html
```

For static hosting, publish this public repository with `index.html` at the site
root. Keep `.nojekyll` when using GitHub Pages so source files remain accessible.
The live site is published automatically from the root of the `main` branch.
The private research checkout and its old Git history are not part of this repository.

## What the numbers mean

- Each line has an exact query and a service role: CPE, ACS, mixed or unknown.
  All collected lines are shown by default; role filters select the desired scope.
- Queries, variants, port slices and related component families can overlap.
  The counter sums selected query matches and can count the same host more than once.
  Badges distinguish families, subfamilies, HTTP components, slices and interfaces.
- The `port:7547` denominator covers that port. Some signature queries cover all
  ports; their totals are not directly comparable with that denominator.
- Country is Shodan IP geolocation. An organization label describes the indexed
  network, not necessarily the device manufacturer, owner or retail brand.
- Country/operator/ASN facets have finite limits. The atlas reports coverage and
  the unassigned tail; a missing slice is not a zero result.
- Missing HTTP evidence can reflect filtering, crawler coverage, stale records,
  or other causes. It does not establish that TR-069 is absent.
- Software banners, shared templates and version labels do not establish
  vulnerability, device model, firmware identity or exploitability.

Read [METHOD.md](METHOD.md) for the evidence model and limitations.

## Rebuild and test

Use Python 3.10+ and a current Node.js runtime. The builder and Count collector
use the Python standard library. No Shodan credentials are needed to rebuild or
test a saved dataset.

```bash
python3 tools/build-map.py
python3 tests/test_build_map.py
python3 tests/test_collect_map.py
python3 tests/test_sync_facts.py
python3 tests/test_index_comparison.py
node tests/atlas-audit.mjs index.html
node tests/atlas-audit.mjs atlas/tr-atlas.html
node --test tests/map-gestures.mjs tests/network-gestures.mjs tests/network-connections.mjs tests/snapshot-navigation.mjs
python3 tools/audit-publication.py
```

The builder selects the latest completed, error-free snapshot. To build another
date, pass its directory; use `--output-dir DIR` for an isolated output.
Edit `atlas/map-template.html`, then rebuild both entry points.

Use the date selector in the atlas header to open the best completed collection
for each UTC day. Full country sweeps take precedence, followed by coverage of
lines, operator slices and research queries; the later run breaks a tie. October 8
uses 22:27 UTC and October 10 uses 10:21 UTC. Other runs remain archived and old
shared URLs retain their exact measurements. The URL keeps the chosen
snapshot, language, map filters and network view; browser Back restores the
previous selection. Signatures absent from an older collection remain selectable
with unavailable counts rather than falling back to the whole map.

The build also generates compact measurement files in `atlas/snapshots/`. Publish
that directory alongside the HTML files. Historical dates load these files from
the same site; the embedded snapshot still opens offline. News, attribution and
the documented ACS relationships use the current editorial catalog, with their
own evidence dates. Switching snapshots changes measured counts and operator
observations, not the revision of those documents.

## Collect fresh aggregates

The collector only calls Shodan's `/shodan/host/count` API; it does not send
requests to devices or download host records. Shodan documents that this endpoint
returns totals/facets without consuming query credits. An API key and applicable
account access/rate limits still apply. [Shodan API reference](https://developer.shodan.io/api#shodan-host-count).

Credentials come from `SHODAN_API_KEY` or the initialized Shodan CLI configuration:
`~/.shodan/api_key` when `~/.shodan` exists, otherwise `~/.config/shodan/api_key`.
`--shodan-config-dir DIR` overrides the directory. Never commit credentials.

```bash
# Inspect the complete plan without a key, network access or writes.
python3 tools/collect-map.py --dry-run

# Fresh daily collection; a new UTC timestamped directory is created each time.
python3 tools/collect-map.py --build

# Continue the exact saved scope, queries and limits after interruption.
python3 tools/collect-map.py --resume data/mapdata/snapshot-YYYYMMDD-HHMMSS --build

# Copy a completed snapshot and refresh selected lines in a new directory.
python3 tools/collect-map.py --from-snapshot SOURCE --output-dir NEW   --only cwmp-server,telefonica-cwmpweb --skip-variants --build

# Collect only research queries; standalone runs go under data/research/.
python3 tools/collect-map.py --queries-only
```

Defaults cover every registry line and every returned country, with top-100
organization and ASN facets per pair. Requests are paced at least 1.1 seconds
apart; transient failures are retried and never converted into zero counts.
`--max-requests N` pauses after N HTTP attempts. Exit codes: 0 success, 1 failure,
3 paused, 130 interrupted. Only one collector can run in a checkout at a time.
A completed `--resume` is a no-op. `--drill-only` is a legacy in-place operation;
use a new snapshot for daily history. No daily scheduler is installed by this repo.

`--drill-lines` and `--drill-countries` limit the sweep; zero means all.
`--query-group` selects catalog groups. `--skip-variants` omits research queries.
The resume plan freezes these choices, including query text and facets.

## CPE–ACS graph

Open the **CPE ↔ ACS** tab or [link directly to it](index.html#lang=en&tab=ecosystem).
**Observed networks** builds country–organization–signature combinations from
the saved snapshot. Switch between the interactive network, flow overview and matrix; filter countries,
operators, signatures and service roles, or combine documented corporate groups.
Connections link to exact measurements and map selections. Mobile users retain
the interactive graph with pan, pinch zoom and full-screen mode, plus a scrollable matrix. See [DEPLOYMENTS.md](DEPLOYMENTS.md).

**ACS evidence** contains the curated integration and configuration graph from
`data/acs-relations.json`. Its sources, translations and references are validated
at build time. Hypotheses are optional. Shared links preserve both views' filters
and selections. See the [integration matrix](ACS-INTEGRATION-EVIDENCE.md) for the
catalog schema. The reviewed operator aliases and groups are maintained in
`data/operator-catalog.json`; unrecognized organization labels remain unassigned.

## Data and evidence

| File | Purpose |
| --- | --- |
| [registry.csv](registry.csv) | Stable line IDs, roles and exact queries; its editorial baseline is dated |
| [data/collection-queries.json](data/collection-queries.json) | Versioned variants, parent lines, facets and research sources |
| [data/mapdata/history.json](data/mapdata/history.json) | Snapshot status index and latest completed collection |
| [data/mapdata/facts.json](data/mapdata/facts.json) | Current observation counts, dates and response references |
| [data/operator-catalog.json](data/operator-catalog.json) | Exact country-scoped operator aliases and sourced corporate groups |
| [data/acs-relations.json](data/acs-relations.json) | CPE–ACS relationship graph, evidence status, dates and sources |
| [data/mapmeta.json](data/mapmeta.json) | Attribution, findings, limitations and source links |
| [data/index-comparison.json](data/index-comparison.json) | Independent FOFA research aggregates and fixed Shodan reference counts |
| [data/research-findings.json](data/research-findings.json) | Research-to-atlas coverage and explicitly withheld categories |
| [data/project-news.json](data/project-news.json) | Dated developments with supporting files |
| [data/wanted.json](data/wanted.json) | Community firmware searches, evidence gaps, review status and translations; generates WANTED.md |
| [data/attribution-evidence.json](data/attribution-evidence.json) | Direct public code and firmware anchors, pinned commits, matching markers and file hashes; generates [ATTRIBUTIONS.md](ATTRIBUTIONS.md) |
| [LEGACY-HTTP.md](LEGACY-HTTP.md) | RomPager, mini_httpd, all-port slices and suspected honeypots |
| [TR-PARK-REGISTRY.md](TR-PARK-REGISTRY.md) | Human-readable registry from the current collection |

Each response records its query, UTC collection time and run ID. Completed fresh
full collections update `facts.json` atomically. The initial research count is
retained as `historical_count`; prose is preserved. Missing, mismatched or older
results cannot partially replace current facts. For an already completed full
run, use `python3 tools/sync-facts.py SNAPSHOT_DIR` without API access.

Historical aggregate totals and response timestamps are preserved in this public
edition. Private editorial text embedded in old collection plans is replaced by the public edition;
rebuilding an old date uses the current public notes. All 93 research queries from the full October 10 run are included. Original
manifest counters describe the collection; `publication_redactions` records
editorial changes in the public export. Private firmware, raw host
exports, operational logs and restricted probe packages are not distributed.

## Research notes

- [PUBLIC-DISCLOSURES.md](PUBLIC-DISCLOSURES.md): published findings and fixes relevant to the atlas, including GenieACS, FreeACS and icwmp (iopsys).
- [DEANON-IGDAUTH.md](DEANON-IGDAUTH.md): Broadcom CMS tr69c attribution, pinned binary evidence and hash.
- [CROSS-INDEX.md](CROSS-INDEX.md): separately dated FOFA/Shodan comparison and query scopes.
- [FINGERPRINTS.md](FINGERPRINTS.md): passive markers and authorized active research results.
- [NOTES.md](NOTES.md): public research chronology and corrections.
- [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md): component lineage and attribution limits.
- [DEANON-HUAWEI-CR.md](DEANON-HUAWEI-CR.md): authentication and port/operator slices.
- [DEANON-OBUSPA.md](DEANON-OBUSPA.md): USP transport fingerprints and obuspa attribution limits.
- [ACS-INTEGRATION-EVIDENCE.md](ACS-INTEGRATION-EVIDENCE.md): CPE–ACS graph and evidence matrix.
- [ACS-URL-MINING.md](ACS-URL-MINING.md): firmware configuration records and provenance.
- [ACS-LANDSCAPE.md](ACS-LANDSCAPE.md): the public Bad CPE threat model.
- [ACS-HUNT.md](ACS-HUNT.md): ACS identification and unresolved signatures.
- [NONCE-PATHOLOGY.md](NONCE-PATHOLOGY.md): interpretation limits and disclosure boundary.
- [TODO.md](TODO.md): completed integration work and open research questions.

These are edited English public editions. Research-time measurements are labeled
as historical; current counts come from snapshots. Passive and active fingerprinting results are in scope. New vulnerability
findings and associated reproduction details are excluded from documents,
embedded data and Git history. The separate `probes` package is not distributed.

The [publication review](reports/PUBLICATION-REVIEW-2026-10-10.md) records the
reviewed scope, exclusions and validation.

## Contributions

For firmware leads and fingerprint evidence, start with [Bring Your Own TR-069](WANTED.md).

A new finding should include an exact query, observation date, source, service
role and confidence level. Add its query to the catalog, its public explanation
to the notes, and a dated news entry. Keep all four interface languages complete.
Do not add device addresses, credentials, firmware or unpublished advisories.

The manifesto is the single pinned news item (`pinned: true`). It stays first
and opens the news ticker. Published vulnerability reports (`kind: "disclosure"`)
and major research entries (`important: true`, including Bad CPE) follow it, with
amber cards and an Important label. Ordinary news follows this group. Each group
is ordered by date, newest first; the map ticker uses the same order and emphasis.

## License and third-party sources

Project-owned code and documentation are licensed under the
[Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for attribution and source-data
scope. The map uses Natural Earth public-domain geometry. Shodan aggregates and
third-party names retain their respective rights and applicable terms.
