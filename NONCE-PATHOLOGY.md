# Authentication-response research: public scope

Public edition, 10 October 2026. The project has a separate private research log
covering authentication-response patterns. Detailed nonce-generation analyses,
implementation offsets, reproduction instructions and unpublished advisory claims
are excluded from this publication.

## What the atlas establishes

The public atlas counts observable signatures and response variants. It can show
Basic/Digest markers, protocol families and version strings, with exact query
scope and collection dates. Those observations do not constitute a vulnerability
census. Signature counts must not be labeled affected-device counts.

Repeated values in a few cached responses do not establish a constant across an
entire population or across reboots. Uniqueness in a sample does not establish
cryptographic unpredictability. A shared response template does not prove shared
authentication-validation code. A version string does not identify all backports.

[HTTP Digest, RFC 7616](https://www.rfc-editor.org/rfc/rfc7616.html) discusses
nonce handling and replay considerations. Evaluating a particular implementation
requires evidence about validation, state and deployment conditions; a banner
pattern alone cannot demonstrate authentication bypass or replay.

## Evidence retained publicly

- [METHOD.md](METHOD.md): measurement and attribution limits.
- [DEANON-HUAWEI-CR.md](DEANON-HUAWEI-CR.md): bounded negative observations.
- [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md): component-family evidence.
- [ACS-HUNT.md](ACS-HUNT.md): unresolved vendor and service-role questions.

## Observable fingerprint classes

| Line | Public response marker | Interpretation |
| --- | --- | --- |
| easycwmp | `realm@easycwmp` and the collected opaque marker | Related family queries overlap |
| TR069 Client | Server/realm text, Basic or Digest, qop and header layout | Variants need not be disjoint |
| Sercomm / TI classes | Vendor-branded realms and decimal nonce text | Format alone does not prove security properties |
| HuaweiHomeGateway | Realm and authentication/port variants | Sample uniqueness does not prove cryptographic strength |
| ACSSimTool | Realm and the exact response value in the query catalog | A sample marker, not a fleet-wide replay claim |
| IgdAuthentication | Realm and structured Base64 text | Manufacturer and validation behavior require separate evidence |

The ACSSimTool sample-marker query is collected separately from the realm query.
Its count measures matching indexed responses. It is not evidence of shared
credentials, a universal constant, or successful authentication replay.

The public scope includes passive Shodan fingerprints and active fingerprinting
results. New vulnerability findings and their implementation or reproduction
details remain private. The separate `probes` package is excluded.
