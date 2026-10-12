# HuaweiHomeGateway: authentication and port slices

Public research edition, 10 October 2026. The vendor is explicit in the realm;
the investigation concerns response variants and operator distribution, not
identification of a single hardware model.

## Response signature

```http
HTTP/1.1 401 Unauthorized
Connection: Keep-Alive
WWW-Authenticate: Digest realm="HuaweiHomeGateway",nonce="<redacted>", qop="auth", algorithm="MD5"
Content-Length: 0
```

The inspected responses have no Server header, Date header or body. Spacing before
nonce differs from spacing before qop and algorithm. A Basic variant uses the same
realm. These observations describe inspected samples, not every implementation.

## Historical census

Research-time Count measurements from October 10, before the publication refresh:

| Slice | Query matches |
| --- | ---: |
| Port 7547 | 2,645,752 |
| Digest, all ports | 2,837,190 |
| Basic, all ports | 32,468 |
| Port 8081 | 101,168 |
| Port 51005 | 81,004 |
| Port 8080 | 9,360 |
| Basic in Germany | 22,720 |
| Digest in Germany | 48,102 |
| Basic outside Germany | 9,747 |

Current counts and dates are in [facts.json](data/mapdata/facts.json) and the
[query catalog](data/collection-queries.json). Rows overlap and are not additive.

## Auxiliary-port correction

The former description of all non-7547 matches as web interfaces was incorrect.
A 300-banner auxiliary-port sample contained the same authentication-server
pattern, with no model names or HTML titles. The atlas now describes this as
port distribution outside 7547. In a 40-host follow-up, 33 records exposed only
one service: shared response patterns do not imply the same physical hosts.

## Operator slices

| Port or variant | Research association | Limit |
| --- | --- | --- |
| 8081 | Spark/Vodafone networks in New Zealand; about 98% NZ in the historical slice | Does not assign individual ONT models |
| 51005 and 8083 | OTE/Cosmote in Greece | Operator-associated slice |
| 8080 | Eir/SIRO in Ireland | Operator-associated slice |
| 30008 | Australian NBN networks | Multiple CPE possibilities |
| 10302 | Telia/Bahnhof networks in Sweden | No model established |
| 7548 | Orange in France | No model established |
| Basic in DE | AS3320/Deutsche Telekom | Also contains Digest responses |
| Basic in SA | Saudi network slice | Coexists with a much larger Digest slice |

Public procurement lists can suggest model candidates, but they do not label
individual matches. Basic and Digest coexistence can reflect configuration as
well as implementation differences; it is not by itself proof of two generations.

## Negative result and evidence limits

A nonce uniqueness check reported 593 distinct values in 593 inspected responses,
including 63 groups collected in the same second. No tested repetition pattern
was found. This is a sample-limited negative, not proof of cryptographic security.
Detailed security evaluation is outside the public atlas release.

Firmware inspection of one HG8145V5 image (October 2026) independently supports
two of the observed traits: the connection-request listener is configured on
port 30005 in the shipped configuration, and the nonce path draws from the
operating-system random device. This is implementation evidence for the
platform family, not for every indexed match.

Uniform responses do not distinguish HG8245, HG8247, HG8310 or EchoLife models.
The atlas records ports, authentication modes and operator facets without claiming
that model-level decomposition has been achieved.

## Atlas integration

The Huawei line, 24 catalog queries, dated observation cards and a project-news
entry retain these results. See [METHOD.md](METHOD.md) for scope rules and
[TR-PARK-REGISTRY.md](TR-PARK-REGISTRY.md#huaweihomegateway-cr-slice) for the line.
