# Comparing Shodan and FOFA observations

Research date: 13 October 2026. Public review: 15 October 2026.

The atlas carries a separate [aggregate comparison dataset](data/index-comparison.json):
13 signature queries and 22 country slices on port 7547. It is shown under
Observations and remains fixed when the map's snapshot or filters change.
The map, network and headline counters continue to use their selected Shodan
snapshot. FOFA values are never added to those counters.

<a id="method"></a>
## Provenance and scope

FOFA values are transcribed from the dated research summary. Exact retrieval
timestamps and index-window filters were not retained. Query strings are the
summary's notation, not verified API requests: in particular the Gateway entry
contains ambiguous nested quotation marks. Country rows retain the country
and port scope, but not the original request string. The public dataset contains
aggregate counts only.

The comparison uses Shodan's saved `20261013-160503` snapshot, with each
record's query and timestamp retained. These are reproducible reference values,
not the older Shodan estimates quoted during the FOFA research. The two engines
were not queried simultaneously. Their indexing, query semantics and retention
windows differ. Several pairs also have visibly different scopes: FOFA's Gateway
notation is all-port while the atlas's main Gateway query selects port 7170;
`YAPS` and `YapsieWorld` are different strings.

Read each pair as two observations with their own query. Counts may overlap
within either source. They do not establish unique-device populations, coverage
multipliers or a combined global total. A zero means that the recorded query
returned zero, not that the implementation is absent.

<a id="follow-ups"></a>
## Fingerprint follow-ups

- The DSLForum realm appeared in DE:7170 and SG/GB:8085 contexts as well as
  the German port-7547 population. The FOFA research reports 687,022 matches
  for its DE:7170 realm slice. A gSOAP slice on that port reports 1,207,083;
  the two queries can overlap. Operator samples point to Telefónica Germany.
  They do not establish a manufacturer or a universal operator assignment.
- The Gateway realm appears in Vodafone UK:1024 and Bell Canada:10001
  contexts, alongside the TIM:7170 population. Port ecology justifies separate
  queries, not a claim that the implementations must differ. The TIM component
  attribution stays open.
- Korean port-7547 counts include 4,707,708 FOFA matches, with 157,484 in the
  research's `WWW-Authenticate` subset. The approximately 3.35% proportion
  measures indexed header presence. It is not a response rate, protocol census
  or test of scanner filtering. A separate Korean port-7548 query returned
  7,413 matches.
- The research's CN-labeled port-7547 aggregate was 5,902,772, with 396,785
  authentication-marker matches. Its operator examples include Taiwan, so CN
  is omitted from the country comparison pending geography normalization.
  Sampled non-TR-069 services demonstrate port reuse; their share of the full
  aggregate has not been measured.

The [query catalog](data/collection-queries.json) adds Shodan follow-ups for the
DSLForum and Gateway scopes. New queries are marked uncollected in snapshots
that predate them. A future collection supplies their own dated counts.
