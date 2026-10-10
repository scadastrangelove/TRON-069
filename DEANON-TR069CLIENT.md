# TR069 Client: component lineage and attribution limits

Public research edition, 10 October 2026. The evidence supports an Atheros
openagent-related component family. It does not identify the manufacturer of
every device returned by the main query.

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

The research compared the DigAuth-associated response template with
`AthSDK/apps/openagent-2.0/src/tools/conn_req_server.c` in a D-Link DIR-615 GPL
source release. The distinctive template includes an Apache-style Server string,
Date, Vary and Accept-Ranges headers. A Brazilian port-8081 slice bridges the
TR069 Client Server string and DigAuth realm.

The main population has a shorter response template. The defensible conclusion
is component-family evidence with an unresolved OEM carrier, rather than a
fleet-wide hardware attribution. Source and firmware extracts are retained
privately and are not included in this release.

## Variants overlap

The initial research measurements included approximately 1.65M main-query matches,
852k qop matches and 1.549M matches with nonce following realm. Their overlap means
these cannot be treated as disjoint populations. The latter query is a textual
response marker, not a rigorous logical complement of qop. Historical Basic and
DigAuth-bridge counts were 1,479 and 21,488 respectively.

Current dated counts are collected independently in
[data/collection-queries.json](data/collection-queries.json). Do not add the
main family, DigAuth, fake-Apache, port slices and variants as independent devices.

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

The main line retains a component-class badge. DigAuth and fake-Apache keep their
specific source-backed scope. Variants, Singtel ports and the Brazilian bridge
are collected separately. Research news and observation cards link here and to
[ACS-HUNT.md](ACS-HUNT.md). Unpublished security-audit hypotheses and reproduction
details are excluded pending disclosure clearance.
