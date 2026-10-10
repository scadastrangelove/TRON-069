# Passive and active fingerprinting

Public research edition, 10 October 2026. Fingerprints describe response behavior
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

The historical source comparison and laboratory work recorded these distinctions:

| Observation | Through 1.6.2 | 1.7.0–1.8.6 |
| --- | --- | --- |
| Connection closed with FIN before sending request bytes | 401 challenge | 409 Conflict |
| `Connection: close` on a successful Connection Request response | Absent in inspected code | Present in inspected code |
| Configurable Basic Connection Request mode | Not present in inspected code | Present |

These are coarse behavioral classes within the inspected releases. Forks, patches,
proxies and deployment configuration can alter a response. No distinguishing
fingerprint for every patch release in 1.7.0–1.8.6 was established.

## Historical operator-authorized scan — 7 October 2026

The research log records 29,007 targets checked within an authorized operator
scope in approximately 13 minutes. 19,392 accepted a TCP connection. Of 18,662
easycwmp-associated responders, 18,657 returned the later 409-on-FIN pattern,
four returned the earlier 401-on-FIN pattern, and one returned an unexpected 500.
The four earlier-pattern records also contained the easycwmp realm in the saved
banner evidence. Median recorded latency was 277 ms.

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
