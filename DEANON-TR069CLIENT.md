# TR069 Client: Works Systems OneAgent TR

Public research edition, updated 13 October 2026. The component family is
identified: the connection-request server is **Works Systems OneAgent TR**,
an embeddable TR-069 client licensed to device manufacturers. The
`TR069 client TCP connection request Server` string and the response template
come from this software family, not from any single device vendor.

## Attribution evidence

Three independent legs, all public:

1. **Binary template match.** A public Nokia FastMile 5G Gateway 3.2 dump
   contains `usr/bin/tr_agent` with the complete 401 template at a fixed
   offset — same status line, header order, the exact Server string, and the
   Digest parameter order (`realm`, `qop`, `nonce`, `algorithm`, `domain`)
   as format placeholders. The same binary carries the strings `Workssys`,
   `www.workssys.com` and the realm value `TR069 Client`.
2. **Build-tree naming.** ASUS asuswrt trees ship `apps/private/tr069` whose
   headers carry `Copyright(c) 2009, Works Systems, Inc.`, a
   `TR069_CLIENT_VERSION "TR069 Client 1.0"` define, and a build script that
   prints `Compile OneAgent-TR successful`. A prebuilt ASUS `tr` binary
   contains the same Server string and template.
3. **Source lineage.** The Atheros AthSDK `openagent-2.0` source (published
   in the D-Link DIR-615 GPL release) carries
   `Copyright(c) 2006-2007, Works Systems, Inc.` — the same software house,
   earlier code line. The previously established openagent lineage and
   today's OneAgent identification point to the same component supplier.

Vendor documentation of the era describes OneAgent TR as a ready-to-integrate
TR-069 client for xDSL/cable/xPON/Wi-Fi CPE across Linux, VxWorks and Windows
CE, which matches the observed spread across unrelated operators and
continents. See the [OneAgent TR datasheet](https://valuetechsa.com/download/OneAgent%20TR-datasheet.pdf)
and the [Wind River IDP XT guide](https://www.intel.com.br/content/dam/www/public/us/en/documents/guides/wind-river-idp-xt2-programmers-guide.pdf),
which lists the `wr-wks-oneagent-tr069` ISV layer.

<a id="public-evidence"></a>
### Reproducible public sources

Checked on 13 October 2026. Repository links are pinned to commits; offsets
are hexadecimal byte offsets in the named files. Firmware and third-party
source code are not redistributed in this repository.

| Evidence | Public source | Marker |
| --- | --- | --- |
| Nokia FastMile 5G Gateway 3.2 | [natumbri firmware dump, `usr/bin/tr_agent`](https://github.com/natumbri/FastMile_5G_Gateway_3.2/blob/3bb8cce2dcf74e97a292574bbfc69a811bb5e7ea/firmware/usr/bin/tr_agent) | Complete 401 template at `0x92440`; Digest order `realm, qop, nonce, algorithm, domain`; `Workssys` at `0x9e798`, `www.workssys.com` at `0x9eac0` |
| ASUS source headers | [asuswrt `include/tr.h`](https://github.com/smx-smx/asuswrt-rt/blob/81404a37312b7707c29de12c3a38ef7e50eea3c8/apps/private/tr069/include/tr.h#L3) | Works Systems copyright (2009); `TR069_CLIENT_VERSION` at line 169 |
| ASUS product name | [asuswrt `Makefile.DSL_ASUSWRT`](https://github.com/smx-smx/asuswrt-rt/blob/81404a37312b7707c29de12c3a38ef7e50eea3c8/apps/private/tr069/Makefile.DSL_ASUSWRT#L82) | `Compile OneAgent-TR successful` |
| ASUS prebuilt | [asuswrt-merlin `prebuild/tr`](https://github.com/gnuton/asuswrt-merlin.ng/blob/14166d1af5fc9a115c66f187e1618977b732682d/release/src/router/tr069/prebuild/tr) | 401 template at `0x7cd95`; Digest order `realm, nonce, algorithm, domain`, with no qop placeholder |
| Earlier openagent branch | [DIR-615 AthSDK `conn_req_server.c`](https://github.com/nist/DIR-615/blob/272e8bbe56907d3d89e8409f4de1552b63055823/GPL_Source_Code/src/AthSDK/apps/openagent-2.0/src/tools/conn_req_server.c#L2) | Works Systems copyright (2006–2007) |

SHA-256 of the inspected binaries, also verified against these public copies:

```text
c964db3a877d8a0d58ac7531b8b1caab2faaeba81de4d9192ad6be24651880ed  Nokia tr_agent (839680 bytes)
6ccb9cf73731b4eb70a264b845bce477512f468fbda329b98f58815b61b55d94  ASUS tr (592168 bytes)
```

## What the attribution does and does not give

- The full `Server` value is the primary marker; the realm alone is weaker.
- `qop="auth"` presence is a **build variant**, not an operator trait: one
  inspected binary family emits it, another does not. The fleet's qop split
  should be read as build variants of the component.
- `TR069 Client 1.0` is a fixed user-agent-style string, not a product
  version.
- **The hardware OEM is not derivable from this response.** Any specific
  device may also carry a manufacturer-modified branch of the component.
- A caution: nmap associates the different `TR069 client CLI Server` string
  with one specific Alcatel-Lucent ONT; that hardware mapping must not be
  transferred to this line.

Device OEM carriers remain a separate, secondary question.

## Version discrimination

The response distinguishes **build variants, not product versions**. Two
challenge-template families exist at compile time — with a `qop` placeholder
(matched in the Nokia binary) and without it (matched in the ASUS prebuilt).
These provide binary anchors for the observed qop/no-qop split; the qop
value itself is runtime configuration. Authentication mode (Digest/Basic) and
the `domain` value (for example `/`, `/tr069`) are per-deployment settings.
The `TR069 Client 1.0` string is a fixed user-agent constant present across
years of builds and does not encode a version. Both known binaries also carry
a second handler (`TR069 client CLI Server`) whose response content differs
by build; that endpoint, where exposed, is a finer discriminator.

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
related variant uses `TR069 client TCP connection request Server` as its
Server header value. A Brazilian port-8081 slice
carries both markers in one response — the bridge confirms both sub-families
derive from the same code base.

The main population uses a shorter response template (Date, Vary and
Accept-Ranges headers removed), matching the OneAgent TR binaries above.
The openagent-2.0 source identifies Works Systems as the author; Atheros
AthSDK and the DIR-615 release are distribution paths. The fingerprint
identifies the licensed component. Device models require separate evidence.

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

| Feature | Sub-family A (Works Systems openagent-2.0) | Sub-family B (Works Systems OneAgent TR) |
| --- | --- | --- |
| Realm | `DigAuth` | `TR069 Client` |
| Server header | `Apache/2.0.40 (Red Hat Linux)` (imitation) | `TR069 client TCP connection request Server` |
| Nonce length | 64 base64 characters | 31 base64 characters |
| Date header | Present (provides a timing reference) | Absent |
| Vary / Accept-Ranges | Present | Absent |
| Content-Type | `text/html; charset=ISO-8859-1` | Absent (Content-Length: 0 only) |
| Observed on | BR port 8081; small ISPs | Main fleet: Charter, EBOX, Maroc, Vivo, Singtel |
| qop variant | `qop="auth"` in the inspected source template | Build templates with/without qop; Basic also observed |

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

A stratified 38-host re-check (October 13) of cached host records found only
port 7547 for the sampled United States, Canadian and Moroccan matches;
Singapore hosts show only the same component's port family (1024/1025/1026, 30005,
30002). A Dutch consumer-network pocket (KPN) carries the component on ports
9000/9002/9016 — a distinct port ecology and an operator whose issued-hardware
history supplied model candidates. One cloud-hosted address had roughly a
thousand indexed services, including this banner, consistent with emulation.
Such matches require review before treating them as physical CPE.

## Bounded negative results

| Candidate inspected | Result | Scope |
| --- | --- | --- |
| Sercomm RV6699 v4-RT and RV6688v2-MTS | Main Server string not found | These builds only; a menu label is not a component identification |
| Sagemcom F@st 3864OP | String absent; response layout differed | Inspected image only |
| ZTE H108N and H298N | Main string absent; other ZTE components present | Inspected generations only |
| ZTE F670L (V1.1.20P3N4D full root filesystem + V9.0.11P1N36 httpd) | Server literal and realm not found, October 13 | These inspected artifacts only |
| Huawei HG8145V5 (cwmp, six CWMP libraries, full root filesystem) | Server literal and realm not found, October 13 | Inspected image only |
| Three Netis retail builds | TR-069 component not found | Operator builds remain a possible explanation of the CLI Server line |
| Four RAC2V1K repositories | No stock root filesystem found | Does not prove that no stock image exists elsewhere |

The CLI Server naming resemblance is supporting evidence only. Qualcomm-based
hardware is compatible with the component hypothesis but is not proof of it.

### ODM lead and closed acquisition hunts

EZpacket Agent4.0 remains a likely distribution relative. The public
[LC4 TR-069 package](https://github.com/jhbsz/LC4/tree/6cdd53f2c112c47485fe4ad73feec91b789e09f5/package/tr069)
contains build traces and object names shared with openagent. A matching
Agent4.0 response template has not been obtained, so this stays a hypothesis.

The RAC2V1K, F609/F612 and Arcadyan BRN acquisition hunts are closed for the
component-attribution question. They are no longer prerequisites for naming
OneAgent TR; their earlier negative and inconclusive results remain above.

## Atlas integration

The main line carries a proven Works Systems OneAgent TR component badge.
DigAuth and fake-Apache identify the earlier Works Systems openagent branch
distributed through AthSDK. Variants, Singtel ports and the Brazilian bridge
are collected separately. Research news and observation cards link here and to
[ACS-HUNT.md](ACS-HUNT.md). Unpublished security-audit hypotheses and reproduction
details are excluded pending disclosure clearance.
