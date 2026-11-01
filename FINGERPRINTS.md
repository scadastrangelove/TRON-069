# Passive and active fingerprinting

Public research edition, updated 15 October 2026. Fingerprints describe response behavior
and implementation families. They are not vulnerability tests or affected-device
counts. The shipped collector reads Shodan Count; it does not perform these active
experiments. The separate probe implementation is not included.

## easycwmp source comparison

The research compared 44 release tags in the
[upstream easycwmp repository](https://github.com/pivasoftware/easycwmp), through
1.8.6. The realm `realm@easycwmp` and opaque marker
`328458fab28345ae87ab3210a8513b14eff452a2` were stable across that comparison.
These markers identify a family, not a patch release. A changed marker can support
a fork hypothesis, but configurable or copied responses require additional evidence.

The October 13 review checked these distinctions directly in the upstream
[1.6.2 handler](https://github.com/pivasoftware/easycwmp/blob/EasyCwmp-1.6.2/src/http.c)
and [1.7.0 handler](https://github.com/pivasoftware/easycwmp/blob/EasyCwmp-1.7.0/src/http.c):

| Observation | 1.6.2 reference | 1.7.0 reference |
| --- | --- | --- |
| TCP write side closed with FIN before sending request bytes | Closes without an HTTP response | 409 Conflict |
| `Connection: close` on a successful Connection Request response | Absent in inspected code | Present in inspected code |
| Configurable Basic Connection Request mode | Not present in inspected code | Present |

In 1.6.2, EOF leaves the read loop through the error path and closes the socket.
In 1.7.0, the empty-buffer branch emits 409. Both handlers use uloop; the
distinction is a handler revision. A 401 response can occur in both releases
after request processing. A 200 response alone does not establish unrestricted
Connection Requests, and no response can also mean an older handler, a timeout
or filtering. Forks, patches and proxies can alter these behaviors. No
fingerprint for every patch release in 1.7.0–1.8.6 was established.

## Historical operator-authorized scan — 7 October 2026

The research log records 29,007 targets checked within an authorized operator
scope in approximately 13 minutes. 19,392 accepted a TCP connection. Of 18,662
easycwmp-associated responders, 18,657 returned 409, four returned 401, and one
returned an unexpected 500. The four 401 records also contained the easycwmp
realm in the saved banner evidence; their versions remain unclassified.
Median recorded latency was 277 ms.

This is a dated scoped experiment, not an Internet-wide version census. Missing
responses do not establish implementation absence, and neither response class
establishes vulnerability. Addresses, credentials and raw operational records are
not distributed. The result is retained as research prose, separately from current
Shodan counts; it cannot be refreshed by the Count collector.

## Registry and query fingerprints

[TR-PARK-REGISTRY.md](TR-PARK-REGISTRY.md) lists the current signature queries and
service roles. [data/collection-queries.json](data/collection-queries.json) keeps
variant queries separate from parent lines. [METHOD.md](METHOD.md) explains
overlap, sampling and attribution limits. No new vulnerability findings or their
reproduction details are part of this public fingerprint collection.

<a id="matching-precedence"></a>
## Specific signatures and generic toolkit matches

When one response matches both a distinctive realm and a generic toolkit banner,
use the specific realm for its primary classification and retain the toolkit as
a secondary observation. For example, a response carrying `Sagemcom TR-069` or
`realtek.com.tw` should not lose that evidence merely because it also advertises
gSOAP. A first-match classifier must evaluate those specific rules before a broad
gSOAP fallback. Independent detectors should retain all matched signatures.

This is a classification rule for an observed response, not a way to deduplicate
Shodan totals. Atlas queries remain independent and may overlap. The aggregate
data do not measure every intersection, so no overlap count is inferred here.

A generic gSOAP banner identifies a toolkit. It does not by itself establish a
TR-069 endpoint, a CPE role, or a manufacturer. The atlas therefore labels the
broad gSOAP line as mixed; the separately identified Telefónica frontend is ACS.
An observed version string is recorded at its advertised precision: `2.7` is not
an exact patch version, and a version label alone is not a vulnerability result.

<a id="dslforum-cpe-management"></a>
## DSLForum CPE Management across operator deployments

The display name is now **DSLForum CPE Management**; stable ID
`dt-speedport-sdk` and query `"DSLForum CPE Management"` are preserved.
The old name implied a supplier and a Deutsche Telekom boundary that the
response evidence does not establish. Research records include German 7547
and 7170 populations, Singtel in Singapore on 8085, and a legacy BT/EE context
in the United Kingdom on 8085. These are follow-up scopes, not model labels.

The challenge parameter order differs from the
[Broadcom tr69c anchor](DEANON-IGDAUTH.md#public-evidence). A generic Apache
banner, a search engine's product tag and an RFC example constant do not
resolve the supplier. The previous shared-SDK inference from the constant
alone remains withdrawn. The [cross-index note](CROSS-INDEX.md#follow-ups)
records the research counts separately from current Shodan measurements.

<a id="apache-response-profiles"></a>
## Apache-branded response profiles

The `dslforum-apache-401` collection variant combines the DSLForum realm text,
`Server: Apache` text and HTTP status 401 across all ports. Country, organization,
ASN and port facets describe this subset of the existing DSLForum line. Search
terms can also match composite banners; this is a response-query cohort, not
proof of Apache httpd, a hardware supplier or a separate device population.

The 1 November 2026 review of the saved classifier corpus found two DSLForum
responses without `Date` and one with it. All three inspected openagent/DigAuth
responses carried `Date`. These small regression samples establish template
variation, not fleet-wide percentages. The Works Systems attribution is grounded
in [source and response-template evidence](DEANON-TR069CLIENT.md), independently
of the Date header.

Header-profile analysis must parse complete saved header blocks, retain header
order and distinguish an absent field from an incomplete capture. Body content
may be stored separately from Shodan's banner text. Neither a missing Date text
search term nor a missing captured body establishes the corresponding wire
behavior. The all-port Count query is collected daily; header-presence profiles
remain a separate sample-analysis task.

<a id="gateway-port-scopes"></a>
## Gateway realm on alternate ports

The main atlas line retains `port:7170 realm="Gateway"`. UK:1024 and
Canada:10001 are separate research variants, prompted by Vodafone and Bell
operator contexts in the second index. A common realm does not prove a shared
implementation; different ports do not prove different implementations.

TIM:7170 attribution remains unresolved. The inspected TIM image used 51007
and did not contain the observed realm. A sibling binary cannot close that
gap; see [ACS-HUNT.md](ACS-HUNT.md). The query catalog preserves the 51007
control and adds the two alternate-port country slices.

<a id="cli-build-classes"></a>
## Companion CLI service: deployment and build classes

The [13 October record](data/mapdata/snapshot-20261013-160503/tr069-client-cli-server-netcore.json)
has 1,861 matches, all on port 1234, the inspected component's compiled default.
The [10 October record](data/mapdata/snapshot-20261010-102121/tr069-client-cli-server-netcore.json)
has 1,855: Serbia contributes 137 matches associated with Telekom Srbija
(AS8400). The CLI handler is a CPE companion service, not an ACS endpoint.
Port observations do not reveal which settings an operator changed.

Sampled deployments in China and Serbia expose a fuller route set than the
sampled US fixed-wireless builds. Route presence distinguishes those inspected
builds; it does not classify every device in a country. Route names, operational
records and security findings are excluded. The catalog adds explicit port-1234,
Serbia and AS8400 scopes for dated passive follow-up.
