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
