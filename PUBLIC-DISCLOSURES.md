# Public research disclosures

This page links published reports relevant to TRON-069. The
[Rust-in-Peace disclosure tracker](https://github.com/scadastrangelove/rust-in-peace/blob/main/DISCLOSURES-PUBLIC.md)
tracks the wider research programme, including reports that remain private.

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
