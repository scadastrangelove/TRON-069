# obuspa and USP transport fingerprints

Public research edition, reviewed 12 October 2026.

The inspected obuspa WebSocket server uses libwebsockets. Its ordinary HTTP
responses supplied no distinct obuspa signature in the earlier review. Transport
negotiation offers more useful markers, with a different attribution scope.

## Observable markers

| Observation | Interpretation | Source |
| --- | --- | --- |
| Successful WebSocket negotiation of `Sec-WebSocket-Protocol: v1.usp` | A USP WebSocket endpoint. The subprotocol is specified for USP implementations generally. | [USP WebSocket binding, R-WS.9](https://usp.technology/specification/index.htm) and [obuspa WebSocket server](https://github.com/BroadbandForum/obuspa/blob/master/src/core/wsserver.c). |
| CoAP resource discovery at `/.well-known/core` returns `rt="bbf.usp.endpoint"`, with `if="bbf.usp.a"` and title `USP Agent` | An advertised USP Agent resource. The strings describe a protocol and role; they do not uniquely identify obuspa. | [obuspa CoAP server](https://github.com/BroadbandForum/obuspa/blob/master/src/core/coap_server.c), resource-discovery response. |
| Generic libwebsockets HTTP error | A library-level hint shared by unrelated applications. | [obuspa WebSocket server](https://github.com/BroadbandForum/obuspa/blob/master/src/core/wsserver.c). |

The inspected [data-model implementation](https://github.com/BroadbandForum/obuspa/blob/master/src/core/device_mtp.c)
sets both CoAP and WebSocket port defaults to 5683. Configuration can change
ports, paths, encryption and enabled transports. Port 5683 alone identifies
neither USP nor obuspa; 7683 has no established universal role in this review.

## Search-index observations

An exploratory Shodan review on 11 October reported generic CoAP responses on
UDP port 5683. The initial assumption that Shodan did not index that transport
was therefore withdrawn. Those banners did not establish a USP population.
No reproducible dated query record accompanies the exploratory totals, so they
are not added to the atlas's measured series.

A successful USP negotiation identifies the supported transport. Failure can
reflect configuration, authentication, filtering or a different transport.
Neither result alone supplies an obuspa fleet count. USP also supports transports
other than CoAP, so the population of indexed CoAP services is not a superset
of all obuspa deployments.

## Atlas integration

The transport findings are recorded in project news and linked as research.
No obuspa or USP count line is added. A future line needs a reproducible query
or authorized measurement dataset, dated source responses, and validation
against other USP implementations. Implementation attribution remains separate
from protocol recognition.

The public repository contains this fingerprint summary. Probe implementations,
operational deployment details and raw host records remain outside it.
