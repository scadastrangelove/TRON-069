# EasyCwmp 1.8.6 security advisory

Published 22 November 2026 by Sergey Gordeychik, SCADA StrangeLove.
The research covered EasyCwmp 1.8.6 at upstream revision
[`6094b86`](https://github.com/pivasoftware/easycwmp/tree/6094b8676bf59e25277958a8291d8fc673251311).
Integrators should review their firmware's actual build, configuration and patches.

## How the agent establishes trust

The Auto Configuration Server (ACS) is authorized to manage the device.
That trust depends on the device authenticating its peer. In the reviewed
configuration, certificate verification is disabled by default. Changing the
ACS URL to HTTPS alone leaves verification disabled (#6). The HTTP client
also permits Basic authentication when the peer requests it (#3).

These findings have distinct consequences. Missing certificate verification
lets an active intermediary on the management connection impersonate the ACS.
Basic authentication can then expose the device's ACS login to that peer.
Impersonation changes the prerequisites for the parameter-handling and transfer
findings below. An operator assessing them must account for an on-path attacker
as well as compromise of the real ACS.

## Findings and operator action

The numbers follow the original report to the maintainer.

| Finding | Scope and impact | Action |
| --- | --- | --- |
| #1, #7, #8 · Management parameters and file transfers | Unsafe handling of ACS-supplied parameters can lead to command execution with the agent's privileges. The transfer paths also lack independent content integrity checks and handle transfer arguments unsafely. | Remove shell interpretation of management inputs, pass arguments separately, and verify the integrity and origin of updates before applying them. |
| #2 · Connection Request authentication | With the local Connection Request credentials unset, the listener accepts a request without authenticating the caller. This can trigger a management session. Example passwords are a separate configuration issue. | Reject connection requests until credentials are configured. Restrict management ingress and verify the rejection behavior on a representative device. |
| #3, #6 · ACS identity and credentials | The default settings allow an unauthenticated peer to be treated as the operator's ACS. Basic authentication can expose reusable credentials to that peer. | Require TLS chain and hostname validation. Verify rejection of an untrusted CA and a mismatched hostname. Restrict the authentication schemes allowed by the client. |
| #4 · Local privilege escalation | A local process can interfere with temporary files later consumed by a privileged operation. This path requires local access and works independently of ACS access. | Create temporary files exclusively inside a private directory with restrictive ownership and permissions. |
| #5 · Decoder bounds | The review identified an out-of-bounds read. Testing established the read only. Information disclosure, privilege escalation and code execution remain unproven for this finding. | Add bounds checks and cover the decoder with regression tests. |
| #9, #10 · Reliability | Startup can hang when a local dependency is unavailable. Some valid parameter strings fail to apply. The demonstrated consequences concern availability and correctness. | Bound startup waits and test round-trip handling of valid parameter strings. |

## Coordination

The reporter contacted Piva Software on 8 October 2026 and proposed a 45-day
coordination window. The general contact mailbox returned SMTP 550 (mailbox
unavailable). The reporter forwarded the report to the sales contact on
10 October. By 22 November the reporter had received no vendor response
or confirmation of a fix. On 21 October,
CERT/CC declined to assign CVEs or coordinate the case (VU#937703).
Its assessment treated the ACS as a trusted role for #1, #4, #7 and #8,
discussed example credentials for #2 and placed #6 outside its current scope.
The response did not address #3. The peer-authentication, fail-open and local
access distinctions above explain the reporter's assessment.

This is an independent project advisory. The reviewed source revision is the
scope of the report. Operators can use the checks above to assess their own
firmware and backports.
