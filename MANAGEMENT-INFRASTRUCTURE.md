# Management infrastructure: profiles, observations and TLS candidates

Reviewed on November 12, 2026. This layer describes discovery evidence and
configuration provenance. It does not assign vulnerability status to a fleet.

## Firmware profiles

The inspected Huawei HG8145V5 platform tree was reported to contain 172
customization profile identifiers and 38 data-model views. Several identifiers
belong to variants of the same operator. Neither number measures deployed
operators, devices or reachable ACS instances. The separate EG8145V5 artifact
remains unverified; see the [specimen inventory](SPECIMENS.md).

The public catalog exports eight reviewed profile/port entries from the research
summary. It contains no management URLs, credentials, command definitions,
security-feature flags or private paths. Original image download provenance,
version and hash remain gaps in the public evidence chain.

| Profile | Reported country | Configured CR port | Operator hint |
| --- | --- | ---: | --- |
| `at` | AT | 30005 | Unresolved |
| `edatel` | CO | 8085 | Edatel |
| `une` | CO | 8085 | UNE |
| `oi2` | BR | 51005 | Oi |
| `teliaest` | EE | 51005 | Telia Estonia |
| `true` | TH | 9090 | True |
| `truerg` | TH | 9090 | True |
| `mongolia` | MN | 10301 | Unresolved |

Country and operator hints are reported mappings. Each needs independent review
against the original configuration and public operator evidence. `at` alone
cannot identify an Austrian operator. Profiles sharing a query share the same
measurement; their counts must not be added together.

For each profile, the collector binds the exact Huawei banner query, configured
port and reported country. Organization facets of that joint query show the
indexed networks. Global organization facets and country facets cannot be joined
as if they were host-level records. An operator label alone does not identify the
device model, firmware profile or ACS software.

## Corrected cross-match

The earlier draft claim of 48 Huawei operator matches and 167 hidden operators
was withdrawn. Its totals for Telecom Argentina, Claro NXT, Rogers and TDC came
from the RDK-B signature. In the November 11 snapshot, the RDK-B/TDC organization
facet contains 50,537 matches, while the Huawei/TDC facet contains 16.

No match in a collected facet means no observation in that query and snapshot.
The reason could include the signature's coverage, a truncated facet, a different
organization label or deployment visibility. It does not establish NAT, CGNAT or
the size of an unobserved population.

### First joint measurements — November 12

The [supplementary snapshot](data/mapdata/snapshot-20261112-150712/manifest.json)
contains these exact Huawei × port × country intersections:

| Country | Port | Matches | Leading organization labels |
| --- | ---: | ---: | --- |
| AT | 30005 | 0 | None in this query |
| CO | 8085 | 0 | None in this query |
| BR | 51005 | 820 | V tal: 738; ALGAR TELECOM S/A: 64 |
| EE | 51005 | 1 | EstNOC OY: 1 |
| TH | 9090 | 9 | INEXT: 3; TRUE INTERNET CORPORATION: 3 |
| MN | 10301 | 0 | None in this query |

The Estonia result does not corroborate the Telia hint. Brazil and Thailand labels
are leads for alias/deployment review. None of these counts identifies the image
or firmware profile installed on a particular device.

## TLS discovery

Certificate-name and issuer-name searches are separate query families:

- `ssl.cert.subject.CN:cwmp`: ACS candidates identified by a protocol name.
- `ssl.cert.issuer.CN:"Telefonica Moviles"`: issuer-name matches across potentially
  different services. A text match is not proof of a common cryptographic CA.
- `ssl.cert.issuer.CN:"Subordinada Telefonica Moviles"`: a narrower issuer-name query.
- `ssl.cert.subject.CN:provisioning`: broad provisioning discovery, including
  services unrelated to CWMP.

The CWMP query also has port slices for 7547, 7548, 443 and 8443. Parent queries and
port slices overlap. The atlas displays one query at a time and never adds these
matches to the CPE-signature counter. Both `cwmp` and `*cwmp*` returned 172 matches
in the query validation on November 12; the catalog uses the simpler expression.

The first collection returned 172 CWMP-name matches, 924 Telefónica issuer-name
matches, 8 subordinate-issuer matches and 3,393 provisioning-name matches. Within
the exact CWMP-name query, port 7547 returned 2 matches and port 7548 returned 1.
The preliminary 39/47 port figures did not reproduce under this query and are
excluded from the CWMP-name layer. The port-443 and port-8443 slices returned 80
and 46 respectively.

Results retain the exact query, collection timestamp, country, organization, ASN,
port and certificate-fingerprint facets. These are Shodan indexed matches,
not a count of unique controllers, unique certificates or devices currently online.
Facet tails are explicit. Historical snapshots without this layer show it as
uncollected. The supplementary collection preserves the original timestamps of
copied fleet measurements.

## Evidence gaps and next steps

1. Publish an independently retrievable image reference, version and hash for the
   Huawei configuration evidence; verify the separate EG8145V5 sample.
2. Deduplicate the 172 profile identifiers and review country/operator aliases.
3. Examine organization facets of each exact Huawei × port × country query.
   Record explicit operator matches only after alias and source review.
4. Verify the cryptographic chain between a bundled trust anchor and observed
   certificates. A bundled CA does not by itself demonstrate certificate pinning.
5. Confirm the service role of CWMP-name candidates using public documentation or
   service evidence. Port numbers and staging names do not prove production ACS.
6. Classify the broad provisioning results before assigning them a protocol role.

The research network keeps configuration, observation and candidate evidence
separate. The data-model views describe parameters exposed by the CPE to ACS;
claims about CPE-to-ACS processing require their own evidence.

Sources: [research notes](NOTES.md#section-9.50),
[Shodan Count API](https://developer.shodan.io/api),
[Shodan certificate facets](https://help.shodan.io/data-analysis/ssl-analysis-by-country),
[Broadband Forum CWMP data model](https://cwmp-data-models.broadband-forum.org/tr-069-1-0-0.html).
