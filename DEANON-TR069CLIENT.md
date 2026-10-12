# TR069 Client: component lineage and attribution limits

Public research edition, reviewed 12 October 2026. Source-template comparison
and a response carrying both families' markers establish component lineage from
the Atheros/Qualcomm openagent-2.0 connection-request server. The source is
`AthSDK/apps/openagent-2.0/src/tools/conn_req_server.c`, published in the D-Link
DIR-615 GPL release. Device OEM carriers remain a separate question.

## Observable response

```http
HTTP/1.1 401 Authorization Required
Content-Length: 0
Server: TR069 client TCP connection request Server
WWW-Authenticate: Digest realm="TR069 Client", nonce="<redacted>", algorithm="MD5", domain="/"
Connection: close
```

Inspected variants include qop, Basic authentication and a 503 busy response in
Singtel auxiliary-port slices. Header order and response layout are useful
fingerprints, but do not establish identical code on all devices.

## Component evidence

The full 401-response template (header order, Apache-imitation Server string,
Date, Vary, Accept-Ranges, Content-Type) in the DigAuth-associated sub-family
matches the structure and literals in `conn_req_server.c` line 700. The
difference is the Server header value, which the OEM fork replaced with
`TR069 client TCP connection request Server`. A Brazilian port-8081 slice
carries both markers in one response — the bridge confirms both sub-families
derive from the same code base.

The main population uses a shorter response template (Date, Vary and
Accept-Ranges headers removed), consistent with a derived OEM build. The
proven component lineage (Atheros openagent-2.0) does not by itself attribute
individual devices to a specific OEM or hardware vendor — device-level
attribution remains open. The GPL source is publicly available; no proprietary
code is reproduced here.

## Variants overlap

The initial research measurements included approximately 1.65M main-query matches,
852k qop matches and 1.549M matches with nonce following realm. Their overlap means
these cannot be treated as disjoint populations. The latter query is a textual
response marker, not a rigorous logical complement of qop. Historical Basic and
DigAuth-bridge counts were 1,479 and 21,488 respectively.

Current dated counts are collected independently in
[data/collection-queries.json](data/collection-queries.json). Do not add the
main family, DigAuth, fake-Apache, port slices and variants as independent devices.

## Sub-family identification (fingerprint guide)

The component family has two observable sub-families, distinguishable from
the response alone:

| Feature | Sub-family A (openagent stock) | Sub-family B (OEM fork) |
| --- | --- | --- |
| Realm | `DigAuth` | `TR069 Client` |
| Server header | `Apache/2.0.40 (Red Hat Linux)` (imitation) | `TR069 client TCP connection request Server` |
| Nonce length | 64 base64 characters | 31 base64 characters |
| Date header | Present (provides a timing reference) | Absent |
| Vary / Accept-Ranges | Present | Absent |
| Content-Type | `text/html; charset=ISO-8859-1` | Absent (Content-Length: 0 only) |
| Observed on | BR port 8081; small ISPs | Main fleet: Charter, EBOX, Maroc, Vivo, Singtel |
| qop variant | Always `qop="auth"` | Operator-dependent (with/without qop, some Basic) |

A Brazilian port-8081 slice carries both the sub-family-B Server string and
the sub-family-A realm in a single response, linking the two sub-families.

The observed 31-character nonce (sub-family B) and 64-character nonce
(sub-family A), together with the realm and header layout, provide additional
fingerprint markers. Their fleet-wide coverage remains to be measured.

## Singtel cross-service observations

Cached host records contained TR069 Client on 1024/1025/1026 alongside
CPE-SERVER/1.0 on 58000. This supports an association with a ZTE component.
It does not prove a specific F609-class device or that both services came from
one firmware image. Earlier Huawei co-observations also had timestamp differences;
address reassignment and forwarding remain alternatives. Device addresses are
omitted from this public edition.

## Bounded negative results

| Candidate inspected | Result | Scope |
| --- | --- | --- |
| Sercomm RV6699 v4-RT and RV6688v2-MTS | Main Server string not found | These builds only; a menu label is not a component identification |
| Sagemcom F@st 3864OP | String absent; response layout differed | Inspected image only |
| ZTE H108N and H298N | Main string absent; other ZTE components present | Inspected generations only |
| ZTE F670L | Container not fully decoded in the documented pass | Inconclusive, not a negative attribution |
| Three Netis retail builds | TR-069 component not found | Operator builds remain a possible explanation of the CLI Server line |
| Four RAC2V1K repositories | No stock root filesystem found | Does not prove that no stock image exists elsewhere |

The CLI Server naming resemblance is supporting evidence only. Qualcomm-based
hardware is compatible with the component hypothesis but is not proof of it.

## Atlas integration

The main line carries an Atheros openagent lineage badge with a note that device OEM carriers are unresolved. DigAuth and fake-Apache keep their
specific source-backed scope. Variants, Singtel ports and the Brazilian bridge
are collected separately. Research news and observation cards link here and to
[ACS-HUNT.md](ACS-HUNT.md). Unpublished security-audit hypotheses and reproduction
details are excluded pending disclosure clearance.
