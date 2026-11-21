# Bad CPE: the managed device as an attack source

Public conceptual model, 11 October 2026.

An ACS receives management traffic from CPE. A compromised or deliberately
hostile CPE can exercise the server-facing protocol through the same channel.
If that traffic compromises the ACS, the server's management authority can
extend the impact to other devices it controls. The possible scope depends on
server isolation, authorization boundaries and provisioning privileges.

```text
Hostile CPE → management session → ACS → managed devices
```

The CPE knows its management server address from its configuration. Internet
visibility describes only part of the ACS attack surface. An ACS absent from a
public search index may still be reachable by devices on an operator network.

<a id="scenario-tracker"></a>
## Scenario tracker

Reviewed 22 November 2026. An atlas pair is confirmed only when the same device and management server were tested together and the stated outcome was observed. None of the seven scenarios meets that threshold yet.

| ID | Scenario | Evidence and scope |
| --- | --- | --- |
| S1 | Fleet identity impersonation | Partial. Shared key material was found in firmware. Its role in client authentication and acceptance as a different subscriber device remain unverified. [Firmware review](PUBLIC-DISCLOSURES.md#zte-f670l-public-scope). |
| S2 | ACS denial of service before authentication | Lab-confirmed and published. Device-side traffic caused worker memory growth and reproducible worker crashes. The measured impact concerns availability. [Public availability advisory](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-r976-f8qf-3hrm). |
| S3 | Firmware substitution during distribution | Separate components. A published report documents unauthorized changes to a file store. A device-side review documents missing integrity checks. Delivery and installation of the changed file on the same managed device remain unverified. [File-store advisory](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-cjv9-7rj9-fp6m). [Device-side review](EASY-CWMP-ADVISORY.md). |
| S4 | Stored XSS in the operator console | Lab-confirmed and published. A device-supplied value was stored and rendered as unescaped HTML in the operator interface. The test covered the console rendering path. [Published console finding](https://github.com/scadastrangelove/freeacs/issues/4). |
| S5 | Memory corruption in a SOAP component | Component lab result. Memory corruption was reproduced in an isolated parser test. Reachability through a deployed ACS configuration and code execution there remain unverified. Project lab review; independent verification pending. |
| S6 | Code execution on the ACS from a device session | Unproven. Reviewed device-facing tests establish availability impact. No test demonstrates control of code execution in the ACS process. |
| S7 | False device reports influence provisioning | Partial. In a lab configuration, device-supplied data was accepted and stored. A resulting change to a provisioning decision or to another device remains unverified. [Lab observations](https://github.com/scadastrangelove/genieacs/security/advisories/GHSA-r976-f8qf-3hrm). |

<a id="management-to-device"></a>
## From management authority to device execution

The downstream ACS → CPE leg also has public examples. RDK-B's
`provisioning-and-management` 2.10.0 includes a
[remote syslog command-injection fix](PUBLIC-DISCLOSURES.md#rdkb-remote-syslog-20261012).
The patch closes a path from a writable management parameter to a shell command
on the device. Where an ACS can write that parameter, compromise of the ACS
can turn its configuration authority into a route to device execution.
This supplies a concrete downstream mechanism for the Bad CPE model; the
initial CPE → ACS compromise is a separate prerequisite.

## What the atlas measures

The map counts dated matches for public fingerprints. The CPE–ACS graph adds
configuration, integration and deployment evidence. Together they support
questions such as which client family is present in an operator network and
which ACS relationships have a documented basis.

The graph does not estimate managed fleet size from exposed admin interfaces.
A client family can connect to many ACS products; an ACS can manage multiple
client families. Organization attribution does not establish a single shared
management server. Node size and edge width therefore carry no fleet counts.

Service roles follow the registry. ACSSimTool, NettyServer and the leanoacs
signature remain CPE-side observations. AVSystem libcwmp identifies a client
component. ACS signatures include GenieACS admin UI, OpenACS, Axiros and
Telefónica cwmpWeb. Current totals and collection dates are available in their
map cards.

## Research context

Hostile-client testing of ACS has prior public research, including Hils and
Böhme's [Watching the Weak Link into Your Home: An Inspection and Monitoring Toolkit for TR-069](https://arxiv.org/abs/2001.02564).
“Bad CPE” is the name used here for this direction of the trust boundary.
New vulnerability findings, affected-version details and reproduction material
remain subject to coordinated disclosure and are absent from this public page.

See the [integration matrix](ACS-INTEGRATION-EVIDENCE.md) and
[configuration evidence](ACS-URL-MINING.md) for the sources behind graph edges.
