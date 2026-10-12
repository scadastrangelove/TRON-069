# ACS configuration evidence from firmware

Public edition, reviewed 11 October 2026.

A CPE's management configuration can reveal the ACS endpoint that the device is
expected to contact. A firmware default, a posted configuration and a running
operator deployment have different scopes. The atlas records each accordingly.

## Endpoint records

| Record | Evidence | Public interpretation |
| --- | --- | --- |
| Technicolor DGA0122 configuration | [Discussion 218](https://github.com/hack-technicolor/hack-technicolor/discussions/218), configuration posted 8 March 2022, includes `acs_url` with hostname `nld-acs.com`; CWMP state is 0. | A documented configuration value. It does not establish TIM ownership, an active session or current service availability. |
| TG789vac v2 VANT-6 2.5.3, iiNet image | Local firmware review, 11 October 2026, reports `setup.iinet.net.au:8881`. | A reported configuration endpoint. Artifact digest and a redacted excerpt are still needed for independent reproduction. Authentication fields are omitted. |
| TG789vac v2 MST 17.2 | Local review also reported `nld-acs.com`. | The image's operator provenance needs verification. No TIM ACS attribution is made from this record. |

The TG789 records belong to Technicolor models. They do not belong to the
`tr069-http-server` line attributed to TP-Link VR1600v. The Gateway port-7170
signature remains a separate research question: the inspected TG789 image used
port 51007 and did not contain the observed realm. See [ACS-HUNT.md](ACS-HUNT.md).

## Other image observations

The local review reported test or placeholder values in the inspected ZTE
H108N/H298N images, a certificate reference in Sercomm RV6699, no production
endpoint in the inspected TP-Link VR1600v files, and an MDM-backed configuration
path for the Sagemcom F@st3864OP client. These are image-specific leads awaiting
public artifact records. They do not establish a vendor-wide provisioning rule
or an operator ACS, so no deployment edges are drawn from them.

## Reproducible extraction record

For each new public record, retain the model, firmware version, image SHA-256,
public image source where redistribution permits, configuration path, field
name, endpoint hostname and port, observation date and a redacted excerpt.
Record whether CWMP was enabled and whether the value was a default, override
or runtime configuration. Strip authentication fields, tokens, private keys,
subscriber identifiers and private host records before publication.

Firmware images and extracted trees remain outside this repository. The public
catalog stores evidence summaries and source references. Configured endpoints
are displayed as text, with links to the evidence rather than to live devices.

## Banner visibility

The exploratory review reported no ACS URL in 200 icwmp and 100 GenieACS banners.
That sample is a historical observation, not a universal absence claim.
A CPE's management URL need not appear in its externally visible HTTP banner.
Operator attribution therefore benefits from configuration records and named
integration documents alongside Shodan's organization facets.

The [CPE–ACS graph](index.html#tab=ecosystem) keeps those evidence types separate.
The general security consequence is described in [Bad CPE](ACS-LANDSCAPE.md).
