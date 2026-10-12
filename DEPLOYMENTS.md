# Observed country–organization–signature combinations

Public edition, 11 October 2026.

The atlas's **CPE ↔ ACS → Observed networks** view uses the saved organization
facets for each country–signature query. The same observations drive the graph,
flow overview, matrix, source cards and exact map selections. No additional Shodan request is
needed to build this view.

## Observation model

An observation retains the signature ID, country, original Shodan organization
label, count and source response. Its query, timestamp, run ID and facet coverage
come from that response under `snapshot-*/org-drill/`. The country and signature
are fixed by the query; the organization facet supplies their measured joint
association. The atlas does not reconstruct a joint distribution from unrelated
marginal facets.

The October 10 snapshot contains 38,107 organization-facet rows across 2,457
country–signature slices: 26,081 CPE, 876 ACS, 8,799 mixed-role and 2,351
unknown-role rows. The view defaults to CPE and offers each service role
separately. These are observation rows, not unique devices or operators.

## Organization names and groups

[data/operator-catalog.json](data/operator-catalog.json) defines stable operator
IDs, country-scoped exact aliases and optional corporate groups. Alias matching
ignores case and surrounding whitespace. It does not use substring heuristics.
Unmatched labels retain a country-scoped raw identity; generic labels such as
`IP pools` are not assigned to BT automatically.

The initial named entries cover BT, TIM, WindTre, Charter, TPG, iiNet, Fidium,
Google Fiber and Consolidated Communications. Named network labels support
organization attribution, not a claim about the owner of every device in the
network. The optional TPG Telecom grouping follows the company's
[brand list](https://www.tpgtelecom.com.au/about-us/our-brands). Every grouped cell
retains its constituent raw labels and counts.

The map's existing broad normalization remains available for ordinary map
navigation. Transitions from the observed-network view use `raw:` organization
selections to reproduce exactly the labels shown in a cell, including grouped
aliases. Selecting both a broad alias and one of its raw members counts that
member once. Shared links preserve the selected raw labels.

## Network, flows and matrix

The **Network** view connects signature nodes to country-scoped organization
nodes. Selecting a node reveals up to eight of its neighbors without replacing
the current graph. Its detail card lists measured connections; **More neighbors**
adds another eight, up to 32 for that node. Up to eight expanded nodes are retained
in a shared link. Country, service-role and search filters still bound the graph.

The initial view starts with the largest observed combinations and other
signatures of those networks, so branches are visible from the outset. **More
connections** increases the base selection from 12 to at most 96. Selecting an
individual connection opens its exact measurement and source record.

The layout settles before display. Dragging a node pins its position; its detail
card can release it. **Arrange** repositions unpinned nodes. Drag the background
to pan, pinch or use the wheel or +/− to zoom, and use **Fit** to see the whole
visible network. Arrow keys pan the focused graph; 0 fits it. Full-screen mode
is available at every viewport size. Small screens keep the interactive graph;
**Details** opens the selected record below it. Node positions and the camera
are local presentation state; shared links retain the expanded neighborhood.

The **Flows** overview arranges the same records as signature → organization →
country. Signature–organization curves carry the original measurement; their
width follows its square root. Organization–country connectors indicate scope
and do not encode a summed device population. Country remains part of each
organization's identity. The view supports panning, zooming and source selection.

The **Matrix** pages through six country–organization columns at a time and
keeps all signatures of the selected service role available for comparison.

Matrix cells distinguish:

- A measured value, with exact query, time, coverage and raw-label breakdown.
- `0`: a complete saved organization facet with no matching label.
- `…`: no matching label in a truncated saved facet; the omitted tail may contain it.
- `—`: the country–signature slice was not collected.

No device-total estimate is obtained by summing overlapping signatures.

## ACS evidence

The **ACS evidence** view retains the curated graph from
[data/acs-relations.json](data/acs-relations.json). Operator nodes can reference
the operator catalog through `operator`. A deployment-specific edge can carry
`scope: {line, country, operator}`; it appears in a measurement card only when
all constituent raw labels resolve to that scoped operator. Grouping a company
with other companies does not widen a deployment claim.

Generic client interoperability and architecture evidence appears under
**Component research**, separately from evidence for the selected combination.
For example, easycwmp interoperability with GenieACS is relevant research but
does not identify the ACS serving a Fidium observation. An unknown ACS remains
explicitly unresolved.

## Collection follow-up

Of the current 2,457 source slices, 239 have an unassigned organization tail.
The existing collector's `--org-limit` can request a larger facet on a new dated
snapshot; use `--from-snapshot` and `--only` to limit refreshes when appropriate.
Inspect the saved facet coverage after collection, since a larger request does
not guarantee a complete response.

The saved organization and ASN facets are independent distributions. Future
organization–ASN–port records require queries constrained to the desired
organization or ASN before collecting the next facet. Such a record must retain
its complete query, timestamp, coverage and parent scope. Aggregate observations
alone do not identify a particular management server.
