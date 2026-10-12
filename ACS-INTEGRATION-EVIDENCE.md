# CPE–ACS integration evidence

Public edition, reviewed 11 October 2026. The atlas graph is backed by
[data/acs-relations.json](data/acs-relations.json).

## Relationship matrix

| Relationship | Evidence type | What the source establishes |
| --- | --- | --- |
| easycwmp → GenieACS | Interoperability | The easycwmp maintainer describes testing with GenieACS; the reporter confirms a working configuration in [issue 128](https://support.easycwmp.org/view.php?id=128). |
| RDK-B CcspTr069Pa → operator ACS | Architecture | [RDKCentral documentation](https://developer.rdkcentral.com/documentation/documentation/rdk_broadband_documentation/components/ccsptr069pa/) describes the TR-069 protocol agent and its connection to an ACS. No operator or ACS product is assigned. |
| MiFibra → ZTE Smart Cloud Platform | Named deployment | ZTE announced a commercial deployment for MiFibra home-CPE management in Peru on [20 December 2024](https://www.zte.com.cn/global/about/news/mifibra-partners-with-zte-to-complete-the-commercial-deployment-of-smart-cloud-platform.html). The announcement does not map the atlas's whole ZTE fingerprint family to SCP. |
| icwmp → BT networks | Operator observation | The [UK organization facets](data/mapdata/snapshot-20261010-102121/org-drill/icwmp-iopsys--GB.json) contain named BT organizations. They do not identify an ACS implementation. |
| Gateway realm on port 7170 → TIM networks | Operator observation | The [Italian organization facets](data/mapdata/snapshot-20261010-102121/org-drill/gateway-realm--IT.json) contain Telecom Italia and TIM names. Component attribution remains open. |
| Technicolor DGA0122 → nld-acs.com | Published configuration | A [public configuration report](https://github.com/hack-technicolor/hack-technicolor/discussions/218) records the hostname with CWMP state 0. Operator ownership and active use are unresolved. |
| TG789vac v2, iiNet image → setup.iinet.net.au:8881 | Reported configuration | The local image review records this endpoint. Public artifact provenance remains incomplete; see [firmware URL mining](ACS-URL-MINING.md). |
| Gateway realm → Technicolor / ADB | Hypothesis | Both remain candidates in [ACS-HUNT.md](ACS-HUNT.md). The inspected TG789 image did not close fingerprint attribution. |

## Reading the graph

CPE, operator, ACS product and configured endpoint are distinct node types.
A relationship records its type, evidence status, date, scope and sources.
Hypotheses are hidden until enabled. Selecting a line-backed node opens the
same dated Shodan measurement used by the map; that count belongs to the
fingerprint query, not to the relationship or to an inferred managed fleet.

An interoperability report establishes that a particular setup worked. A vendor
announcement establishes a named deployment. A configuration value establishes
what an image or configuration contained. Organization facets establish where
Shodan observed a signature. These observations can be combined only when their
models, versions, operators and dates actually match.

## Open attribution work

- Attach exact public URLs and platform evidence to the BT community-log lead
  before using it for a CPE-model or ACS-product attribution.
- Identify ACS products used by the operators of RDK-B devices through named
  deployment or configuration evidence.
- Obtain a reproducible, redacted artifact record for the iiNet image.
- Resolve Gateway/TIM firmware attribution independently of hostname mining.
- Add named GenieACS operator deployments when documented. Internet-visible
  admin interfaces alone do not establish ISP size or customer count.

## Catalog maintenance

`nodes` have stable IDs, a kind, a display name and a four-language description.
Operator nodes can reference the operator catalog through `operator`; edges can
include a precise deployment `scope` as documented in [DEPLOYMENTS.md](DEPLOYMENTS.md).
An optional `line` links to the signature registry. `edges` refer to node IDs
and contain `kind`, `status`, `observed`, `reviewed`, translated `summary` and
`sources`. Sources use either a repository `file` (optionally an explicit HTML
`anchor`) or an HTTPS `url` with a title. An optional `map` selects an exact
registry `line` and `country`.

Supported edge kinds are `interop`, `architecture`, `deployment`,
`configuration`, `operator` and `attribution`. Evidence status is `documented`,
`observed`, `reported` or `hypothesis`. The builder validates IDs, dates,
translations, source paths, URLs, line roles and map targets before generating
both standalone pages. No network access is required to rebuild.

The catalog is editorial evidence reviewed on its own date. Rebuilding an older
measurement snapshot uses the current catalog while retaining the original
measurement timestamps and the sources attached to each relationship.
