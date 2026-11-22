# Public research disclosures

This page links published reports relevant to TRON-069. The
[Rust-in-Peace disclosure tracker](https://github.com/scadastrangelove/rust-in-peace/blob/main/DISCLOSURES-PUBLIC.md)
tracks the wider research programme, including reports that remain private.

<a id="zte-f670l-public-scope"></a>
## ZTE F670L — public research and CVE scope, reviewed 22 November 2026

In our review of the stock **ZXHN F670L V1.1.20P3N4D** firmware, we
independently identified four issues involving factory-mode access, the storage
of embedded secrets, TLS key material and the key used to protect configuration
backups. We reproduced the factory-mode access in isolated emulation and examined
the key material offline. We reported these findings to ZTE PSIRT on **12 October
2026**. PSIRT sent a technical response on **14 October**.

On **27 October**, varun935 published an independent teardown of **F670L
V9.0.10P1N12A** describing the same four areas. The two investigations provide
evidence from different firmware generations.
[Publication history](https://github.com/varun935/Zte-f670l-firmware-teardown/commits/5c76a7cf4859915bf7b454f0fa3cbcad608bef38/).

The three ZTE CVE records published on 7 August list **F689** in the product
field and seven **ZXHN F680V9** builds in the affected-version field.
Coverage of F670L V1.1, F670L V9.0 and F6600P under those identifiers remains
unconfirmed. Operators checking an inventory should match both the product and
the firmware build against the vendor record.
[CVE-2026-49006](https://www.cve.org/CVERecord?id=CVE-2026-49006),
[CVE-2026-49007](https://www.cve.org/CVERecord?id=CVE-2026-49007),
[CVE-2026-49008](https://www.cve.org/CVERecord?id=CVE-2026-49008).

<a id="easycwmp-20261122"></a>
## EasyCwmp 1.8.6 — project advisory, 22 November 2026

The [EasyCwmp advisory](EASY-CWMP-ADVISORY.md) documents ACS peer authentication,
Connection Request authentication with unset credentials, local temporary-file
handling and management-input processing. It includes the tested revision,
operator checks, the limits of the decoder finding and the disclosure timeline.

<a id="icwmp-20261122"></a>
## icwmp — operator update, 22 November 2026

IOPSYS confirmed fixes on its development branch for the six findings in the
[October notice](#iopsys-icwmp-20261020). Operators can use the seven linked
commits to check their downstream firmware or request the backport status from
their supplier. Check the handlers for connection requests, HTTPS transfers,
scheduled downloads and DHCP, and ensure logs exclude credentials. A deployment
assessment requires the firmware revision and its patch history.

<a id="rdkb-remote-syslog-20261012"></a>
## RDK-B — remote syslog command injection fixed in 2.10.0

RDK's `provisioning-and-management` 2.10.0 includes **RDKB-66685**, a public
command-injection fix in remote syslog configuration. Upstream
[PR #359](https://github.com/rdkcentral/provisioning-and-management/pull/359)
was merged on 23 September 2026; the
[2.10.0 tag](https://github.com/rdkcentral/provisioning-and-management/tree/2.10.0)
was created on 12 October at 06:27:32 UTC. The fix is listed in the
[release changelog](https://github.com/rdkcentral/provisioning-and-management/blob/2.10.0/CHANGELOG.md).

The affected management parameter is
`Device.X_CISCO_COM_Diagnostics.Syslog.RemoteLog.Host`.
The patch validates the host, checks its length in the parameter setter, and
replaces `vsystem` with `v_secure_system` when starting syslogd. This is a fix in
the provisioning component shipped alongside the TR-069 agent; the agent's
separate 2.5.0 version does not identify the fixed provisioning code.

This illustrates the **ACS → CPE** leg of the
[Bad CPE model](ACS-LANDSCAPE.md#management-to-device): control over a writable
management parameter can reach command execution on a device. An ACS takeover
would supply that control where the parameter is exposed and writable through
the ACS. The upstream fix establishes this downstream mechanism; a complete
CPE → ACS → fleet chain would also require a way to compromise the ACS.

The atlas links this report to `rdk-b-ccsptr069pa` as RDK-B platform context.
Its fingerprint does not reveal the provisioning component version, build
options or operator patch status. Sources checked on 11 November 2026.

<a id="genieacs-20261020"></a>
## GenieACS — seven advisories published 20 October 2026

On 20 October we published seven security advisories and opened
[upstream PR #423](https://github.com/genieacs/genieacs/pull/423) following
CERT/CC's recommendation. On 22 November, six of the seven were publicly
accessible in the [advisory index](https://github.com/scadastrangelove/genieacs/security/advisories).
The table links those six reports.

| Advisory | Finding |
| --- | --- |
| [GHSA-4cqf-3mxq-h5p2](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-4cqf-3mxq-h5p2) | NBI provisioning scripts and VM sandbox escape: CVE-2025-56015 reproduced on `master`, plus an additional escape variant. |
| [GHSA-f85p-xpvm-2v2g](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-f85p-xpvm-2v2g) | Unauthenticated NBI database queries expose credential hashes and operator secrets. |
| [GHSA-cjv9-7rj9-fp6m](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-cjv9-7rj9-fp6m) | Unauthenticated upload and deletion of files distributed to CPE through the File Server. |
| [GHSA-q8c4-88vj-32ww](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-q8c4-88vj-32ww) | ACS-side SSRF and Connection Request authentication-material disclosure. |
| [GHSA-r976-f8qf-3hrm](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-r976-f8qf-3hrm) | Unbounded request bodies and decompression, plus CWMP worker crashes from device input. |
| [GHSA-4wgx-cx5h-m65h](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-4wgx-cx5h-m65h) | Version 1.2.15 fixed argument injection in `/ping`. The inspected `master` revision lacked the fix. It landed on `master` on [26 October](https://github.com/genieacs/genieacs/commit/6b79d82). |

The reports document isolated-lab testing on `master` at `4aa5cbf` and comparisons
with the release branch. The research used Reproof and Rust-in-Peace. The CWMP
availability and Connection Request findings extend the atlas's
[Bad CPE model](ACS-LANDSCAPE.md); the NBI findings concern access to the
administrative API and its management authority.

### Upstream status on 22 November 2026

| Area | Changes on `master` |
| --- | --- |
| Northbound API (NBI) | The NBI [binds to loopback by default](https://github.com/genieacs/genieacs/commit/d2a89de), [restricts query operators](https://github.com/genieacs/genieacs/commit/94a2643) and [omits password and salt fields from user queries](https://github.com/genieacs/genieacs/commit/26e639b). |
| CWMP workers | The agent-facing service [limits request body size](https://github.com/genieacs/genieacs/commit/d885468). It also handles [inherited command keys](https://github.com/genieacs/genieacs/commit/9a1d499), [mismatched attribute responses](https://github.com/genieacs/genieacs/commit/a7091ea) and [unsupported device requests](https://github.com/genieacs/genieacs/commit/48ad0c6). |
| Setup wizard | The wizard [requires admin credentials](https://github.com/genieacs/genieacs/commit/ba5d52b) and [preserves existing resources](https://github.com/genieacs/genieacs/commit/c9d4a99). |

The latest stable release was [v1.2.16, published 29 March](https://github.com/genieacs/genieacs/releases/tag/v1.2.16).
The [`v1.2` branch was three commits ahead of that tag](https://github.com/genieacs/genieacs/compare/v1.2.16...v1.2).
Its tip was `e773297`, committed on 14 September, before the October and November
changes on `master`. [PR #423](https://github.com/genieacs/genieacs/pull/423) remained open.

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
