# Method: passive TR-069/CWMP measurement

Public edition, reviewed 10 October 2026. This document distinguishes aggregate
collection from the earlier research process. The current collector uses Shodan
Count only. Earlier investigations also inspected cached banners, host records,
public source code and firmware locally; those raw materials are not distributed.
No collection command in this repository contacts subscriber devices.

## 1. What a signature line represents

A line is a reproducible query over an observable response pattern. It may name
a component, a vendor-branded endpoint, an operator segment or a broad class.
It is not automatically a hardware model or a unique device population.

| Evidence axis | Example | Limit |
| --- | --- | --- |
| Authentication realm | `realm@easycwmp`, `authenticate@cwmp` | Can be configurable or reused |
| Opaque marker | easycwmp family marker | Check standards and public examples before treating a constant as unique |
| Server header | `CPE-SERVER/1.0`, `TR069 client TCP connection request Server` | Can be copied or emulated |
| Ports and network distribution | 7170/58000, 30005/49501, 6264 | Operator configuration does not prove manufacturer |
| Response layout and status | Header order, Basic/Digest, 404/503 | Behavior and sampling context matter |

CPE, ACS, mixed and unknown are separate service roles. A shared HTTP toolkit
signature can span multiple roles. A 404 response alone does not establish a role.

## 2. Iterative subtraction

Start with known markers, inspect the remaining indexed responses, cluster the
unknown patterns, then count each candidate independently. Historical opaque
mining found a 584k remainder; roughly 561k matches were associated with additional
patterns such as Sagemcom, ZTE, ecntcwmp, Yapsie and Realtek.

Long or complex negative expressions produced unreliable results in the original
experiments. Use short, incremental queries and positive controls; the observed
working limit of about ten simple exclusions is a project heuristic, not an API
guarantee. Inspect query parsing when syntax is unusual.

A one-word search for Authentication can match a longer realm. It must not be
promoted to a new line merely because its result count is large.

## 3. Country, organization and ASN slices

Operator slices reveal multiple implementations within one network. Historical
examples include Charter, WindTre, Vivo and Telecom Italia. Preserve the query's
scope: a US lighttpd query is broader than a verified CenturyLink-only classifier.
Organization normalization uses country context and exact rules; broad substring
merges can combine unrelated networks.

Quote organization names correctly. A literal backslash before a quote can change
the query and produce an apparent zero. Compare a known positive slice.

## 4. Responses without an HTTP signature

The historical October 8 baseline contained about 34.01M matches on port 7547 and
22.72M with the additional HTTP term. Their difference, about 11.29M, is a category
of missing indexed HTTP evidence. Filtering, collection coverage, stale records
and other causes remain possible. Whitelisting and SYN-proxy explanations are
hypotheses, not measurements of that entire category.

## 5. Aggregate facets

The Count endpoint returns totals and requested facets without host records.
The current collector requests countries, ports, ASNs and organizations as
appropriate. Facet limits are finite; returned coverage and remainder accompany
each result. Do not append a facet size twice (`port:8:8`).

[Shodan's API documentation](https://developer.shodan.io/api#shodan-host-count)
defines Count and its credit behavior. Account access and request limits remain
separate from query-credit consumption.

## 6. Historical banner analysis

A search export contains service records, not a simultaneous inventory of each
host. In an earlier sample the structured HTTP parser omitted authentication
headers present in raw response text in about 9% of records. A classifier should
handle both representations and retain the original evidence privately.

Search-order downloads are not demonstrated random samples. Do not infer
population proportions from a small unstratified export.

## 7. Cross-service observations

Search terms usually constrain one indexed service response. They do not prove
that two services are co-resident. Historical per-IP host lookups can provide
cross-service observations, but timestamps must be compared. Address reassignment,
NAT and port forwarding remain alternatives to a shared firmware image.

In the Singtel investigation, some service timestamps differed by 3–19 days.
Later ZTE co-observations strengthen a component association but do not identify
a specific model or prove that both components ship in one image.

## 8. Coverage evaluation

The October 8 development sample classified 210 of 300 HTTP-bearing records
(70%). An illustrative binomial interval is about 65–75%, but it does not account
for search-order bias or operator clustering. This is classification coverage
within that sample, not measured precision or recall over the Internet.

Applying 70% to the historical HTTP/port denominator ratio gives roughly 47% of
all port matches as an illustrative extrapolation only. A sample used to discover
new rules becomes a regression set. Future evaluation needs a separate labeled,
preferably stratified holdout.

## 9. Attribution and corrections

For a response with several matching signatures, prefer a distinctive realm for
the primary label and retain generic toolkit evidence separately. See the
[matching-precedence rule](FINGERPRINTS.md#matching-precedence). This rule does not
change independent query counts or make their populations disjoint.

Evidence ranges from explicit branding, through shared response templates and
operator associations, to a matching source or firmware artifact. State which
level supports each claim. A matching component does not establish the OEM of
all devices returned by a query.

Check common constants against standards and library examples. The shared
opaque value in DT Speedport and ACSSimTool is an RFC example and therefore does
not prove a shared SDK. Real Apache can advertise the same version string used
by an openagent response template. Bound that marker by context.

Huawei auxiliary-port samples show the same authentication response pattern as
the port-7547 slice; they should not all be labeled web interfaces. Conversely,
that resemblance does not prove the same physical devices or hardware models.

Gateway on port 7170 has a strong TIM association. The inspected Technicolor
image used another port and lacked the observed realm. Vendor attribution remains
open. A printf field width is not an integer's digit count or proof of overflow.

## 10. Protocol interpretation

The [Broadband Forum TR-069 specification](https://www.broadband-forum.org/pdfs/tr-069-1-6-1.pdf)
describes HTTP Connection Requests with authentication and a device-selected URL.
A response to `/` need not represent the behavior of the actual Connection Request
URL. A busy response can be normal. The Connection Request channel is distinct
from the subsequent CPE-to-ACS session; transport properties must be scoped.

[HTTP Digest, RFC 7616](https://www.rfc-editor.org/rfc/rfc7616.html), describes
nonce handling and replay considerations. A visible nonce pattern alone does not
prove replay, credential recovery or authentication bypass. No vulnerability
assessment is inferred from atlas counts.

## 11. Twenty practical checks

| # | Pitfall | Check |
| --- | --- | --- |
| 1 | Complex exclusions return implausible counts | Simplify and use positive controls |
| 2 | One-word realm matches a longer realm | Compare exact response evidence and facets |
| 3 | Multi-term search mistaken for co-hosting | Inspect separately dated host observations |
| 4 | One export record mistaken for a host | Keep the service-record unit explicit |
| 5 | Opaque mining misses Basic/no-opaque | Add independent realm and Server searches |
| 6 | Empty banners treated as absent devices | Report missing HTTP evidence separately |
| 7 | Low regional counts interpreted as low exposure | Account for crawler visibility and filtering |
| 8 | Structured parser loses headers | Compare raw response text privately |
| 9 | Incorrect quote escaping creates zeros | Check a known nonzero query |
| 10 | Facet limit appended twice | Validate the facet string |
| 11 | Human-formatted CSV counts parsed as zero | Validate input; use dated API totals |
| 12 | All-port line compared to one-port denominator | Display both scopes |
| 13 | Specialized behavior expected in ordinary GET banners | Keep active research separate |
| 14 | No neighboring services yields no attribution | Report a sample-limited negative |
| 15 | Standard example treated as family marker | Check common public constants |
| 16 | Search-order sample called random | State selection bias and use a holdout |
| 17 | Match counts called devices | Deduplicate only when the underlying data permit it |
| 18 | Asynchronous host records treated as one image | Compare timestamps and alternatives |
| 19 | Standard behavior called a vulnerability | Check the relevant protocol requirement |
| 20 | Discovery query treated as a precise classifier | Preserve the distinction in notes and labels |

## 12. Reproducibility and limits

The catalog freezes exact query text, stable IDs, facets and provenance into each
run. Resuming restores that plan. Fresh runs create new UTC directories; incomplete
runs do not replace the published dataset. Snapshot counts are observations of
Shodan's index at collection time, not live reachability checks.

The method cannot reliably recover hardware models, firmware versions or hidden
services from uniform banners. Overlapping variants remain separate research
slices and must not be added as independent devices.
