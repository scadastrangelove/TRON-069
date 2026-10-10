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

**Current collection: 10 October 2026.** 52 signature lines, 2,457 country–line
operator slices, 93 research queries and 39 additional observations. Collection
ran from 10:21:21 to 11:11:55 UTC; individual results retain their own timestamps.
These are search matches, not a census of unique devices or vulnerable systems.

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
  Dedicated ACS lines are excluded from the default signature sum.
- Queries, variants, port slices and related component families can overlap.
  Removing known overlaps does not prove the remaining sum is disjoint.
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
node tests/atlas-audit.mjs index.html
node tests/atlas-audit.mjs atlas/tr-atlas.html
python3 tools/audit-publication.py
```

The builder selects the latest completed, error-free snapshot. To build another
date, pass its directory; use `--output-dir DIR` for an isolated output.
Edit `atlas/map-template.html`, then rebuild both entry points.

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

## Data and evidence

| File | Purpose |
| --- | --- |
| [registry.csv](registry.csv) | Stable line IDs, roles and exact queries; its editorial baseline is dated |
| [data/collection-queries.json](data/collection-queries.json) | Versioned variants, parent lines, facets and research sources |
| [data/mapdata/history.json](data/mapdata/history.json) | Snapshot status index and latest completed collection |
| [data/mapdata/facts.json](data/mapdata/facts.json) | Current observation counts, dates and response references |
| [data/mapmeta.json](data/mapmeta.json) | Attribution, findings, limitations and source links |
| [data/research-findings.json](data/research-findings.json) | Research-to-atlas coverage and explicitly withheld categories |
| [data/project-news.json](data/project-news.json) | Dated developments with supporting files |
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

- [FINGERPRINTS.md](FINGERPRINTS.md): passive markers and authorized active research results.
- [NOTES.md](NOTES.md): public research chronology and corrections.
- [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md): component lineage and attribution limits.
- [DEANON-HUAWEI-CR.md](DEANON-HUAWEI-CR.md): authentication and port/operator slices.
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

A new finding should include an exact query, observation date, source, service
role and confidence level. Add its query to the catalog, its public explanation
to the notes, and a dated news entry. Keep all four interface languages complete.
Do not add device addresses, credentials, firmware or unpublished advisories.

The manifesto is the single pinned news item (`pinned: true`). It stays first
above newer dated entries and opens the news ticker; other items remain in
reverse chronological order.

## License and third-party sources

Project-owned code and documentation are licensed under the
[Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for attribution and source-data
scope. The map uses Natural Earth public-domain geometry. Shodan aggregates and
third-party names retain their respective rights and applicable terms.
