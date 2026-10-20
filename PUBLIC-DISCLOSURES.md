# Public research disclosures

This page links published reports relevant to TRON-069. The
[Rust-in-Peace disclosure tracker](https://github.com/scadastrangelove/rust-in-peace/blob/main/DISCLOSURES-PUBLIC.md)
tracks the wider research programme, including reports that remain private.

<a id="genieacs-20261020"></a>
## GenieACS — seven advisories published 20 October 2026

Seven [security advisories](https://github.com/scadastrangelove/genieacs/security/advisories)
and [upstream PR #423](https://github.com/genieacs/genieacs/pull/423) were published
following CERT/CC's recommendation, after the reporter received no maintainer
response. The PR records the coordination context and supplies targeted fixes
and recommendations for changes to authentication and isolation.

| Advisory | Finding |
| --- | --- |
| [GHSA-4cqf-3mxq-h5p2](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-4cqf-3mxq-h5p2) | NBI provisioning scripts and VM sandbox escape: CVE-2025-56015 reproduced on `master`, plus an additional escape variant. |
| [GHSA-f85p-xpvm-2v2g](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-f85p-xpvm-2v2g) | Unauthenticated NBI database queries expose credential hashes and operator secrets. |
| [GHSA-cjv9-7rj9-fp6m](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-cjv9-7rj9-fp6m) | Unauthenticated upload and deletion of files distributed to CPE through the File Server. |
| [GHSA-q8c4-88vj-32ww](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-q8c4-88vj-32ww) | ACS-side SSRF and Connection Request authentication-material disclosure. |
| [GHSA-r976-f8qf-3hrm](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-r976-f8qf-3hrm) | Unbounded request bodies and decompression, plus CWMP worker crashes from device input. |
| [GHSA-4wgx-cx5h-m65h](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-4wgx-cx5h-m65h) | `/ping` argument injection: fixed in the 1.2.15 release line, with the fix missing from the inspected `master`. |
| [GHSA-4v25-9q7x-x86v](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-4v25-9q7x-x86v) | Reflected XML injection through the unencoded `cwmp:ID` response field. |

The reports document isolated-lab testing on `master` at `4aa5cbf` and comparisons
with the release branch. The research used Reproof and Rust-in-Peace. The CWMP
availability and Connection Request findings extend the atlas's
[Bad CPE model](ACS-LANDSCAPE.md); the NBI findings concern access to the
administrative API and its management authority.

Status on 20 October: all seven advisories are public; PR #423 is open.
The PR contains targeted patches and recommendations for the broader design
changes described in the reports.

<a id="iopsys-icwmp-20261020"></a>
## icwmp (iopsys) — fixes confirmed 15 October 2026

On 15 October, iopsys confirmed that all six vulnerabilities reported during
TRON-069 research, together with additional issues in the report, had been
addressed on the `devel` branch. This atlas notice was published on 20 October.

The vendor supplied the following public fix references:

| Finding | Fix commits |
| --- | --- |
| Connection Request authentication bypass | [Clear digest parameters before parsing Authorization](https://dev.iopsys.eu/bbf/icwmp/-/commit/2a55b867f0880ffc704cb5daaf957faa8d012786) |
| TLS certificate verification for HTTPS file transfers | [Verify the TLS peer](https://dev.iopsys.eu/bbf/icwmp/-/commit/08fb8d24ef05e718305f456faba6faf91741b05a) |
| Command injection through Download URL / `macro_engine.sh` | [Use TargetFileName for vendor configuration import](https://dev.iopsys.eu/bbf/icwmp/-/commit/32231b7278aae6851eb495c49d95b6ce0ba4102e); [store downloaded web content at a fixed path](https://dev.iopsys.eu/bbf/icwmp/-/commit/be0720a239960c799af967b1dea2adc2b6b46e94) |
| ScheduleDownload crash | [Fix TimeWindowList parsing](https://dev.iopsys.eu/bbf/icwmp/-/commit/a1e8961a2232a0702c0b5833bec57796ba947934) |
| Connection Request password exposure in logs | [Do not log passwords](https://dev.iopsys.eu/bbf/icwmp/-/commit/c0cd22f9d193ab942296fa4ef7b728bbd3a7f5cd) |
| DHCP option-125 parser buffer overflow | [Fix the parser stack overflow](https://dev.iopsys.eu/bbf/icwmp/-/commit/c60da39366c8cda667b9d34b52e1049ccaa00643) |

Status: vendor-confirmed fixes on `devel`. Public commit references checked on
20 October 2026. Thank you to the iopsys team for the fixes and coordination.

<a id="freeacs-20261012"></a>
## FreeACS — 12 October 2026

Eight findings and one index were published as
[issues #1–#9 on scadastrangelove/freeacs](https://github.com/scadastrangelove/freeacs/issues).
The [index, #9](https://github.com/scadastrangelove/freeacs/issues/9), records the
isolated-lab verification and the use of Reproof and Rust-in-Peace. It also
describes a hostile-CPE path into the management plane, a concrete public case
for the atlas's [Bad CPE model](ACS-LANDSCAPE.md).

The reports were published on the fork because upstream is archived. Their
publication does not establish that a deployment has been fixed, or that every
FreeACS title match is affected. The atlas's `http.title:"FreeACS"` line measures
visible administration-page titles. It is not a count of vulnerable ACS servers
or the devices they manage. Atlas inclusion reviewed on 15 October 2026.
