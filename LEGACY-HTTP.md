# Legacy HTTP components: RomPager and mini_httpd

Reviewed: 21 October 2026. Public fingerprint research; aggregate Shodan Count data only.

The atlas collects both components on **all indexed ports**. Each is a `mixed` service line: embedded management interfaces, other HTTP applications and emulated services can share the same marker. The two populations are excluded from the core TR-069 signature sum. Selecting either line shows its own country and operator distribution.

The [query catalog](data/collection-queries.json) contains version, port and cloud-network slices. Every result retains its exact query and collection time. Country/operator facets describe indexed services; they do not deduplicate physical devices. The full October 21 snapshot collects every registry line and research query afresh. Earlier incremental passes on the same date are retained in history with their original timestamps and query plans.

<a id="rompager"></a>
## RomPager

Registry ID: `rompager`. Base query: `"RomPager"` (all versions, all ports).

The `"RomPager/4.07"` slice follows the version associated with **Misfortune Cookie, CVE-2014-9222**. Check Point documents a flaw in the HTTP implementation and explicitly notes that firmware vendors can backport fixes without updating the advertised version. The atlas therefore measures the version marker; it does not infer that every matching service remains exploitable.

Dedicated port queries cover 80, 443, 7547, 7548, 30005, 51007 and 9022. The base port facet also includes other ports returned by Shodan. Port 7547 is useful CWMP ecosystem context; confirming TR-064 or CWMP requires protocol-specific evidence. The `UPnP/1.0` suffix alone does not identify TR-064.

Sources: [Check Point's Misfortune Cookie FAQ](https://sc1.checkpoint.com/misfortune-cookie/index.html), [Allegro's vendor statement](https://www.allegrosoft.com/wp-content/uploads/Allegro-Press-Misfortune-Cookie-2014.pdf), [CERT/CC VU#561444](https://www.kb.cert.org/vuls/id/561444).

<a id="mini-httpd"></a>
## mini_httpd

Registry ID: `mini-httpd`. Base query: `"mini_httpd"` (all versions, all ports).

[ACME Labs' mini_httpd](https://www.acme.com/software/mini_httpd/) is a general HTTP server. Its appearance in CPE firmware explains its relevance to the atlas. The marker also appears in other products and services, so it does not establish a CPE model, an ACS or a protocol role by itself.

Dedicated port queries cover 80, 443, 7547, 7548, 8080, 8081, 9080, 30005, 51005 and 58000. Version 1.19 has a separate all-port query. The previously investigated AirTies :9080 management interface is CPE-side context, not evidence of an AirTies ACS population. This broad line is not an attribution of every :9080 result to AirTies.

<a id="honeypots"></a>
## Suspected honeypots and cloud-network cohorts

The October 17 research note reports the following evidence in an Aliyun RomPager/4.07 population of approximately 44,370 matches:

- 8,049 matches on port 9022, a long tail of unusual ports, and only 25 on 7547.
- 99 of 100 sampled response banners were byte-identical, advertising `RomPager/4.07 UPnP/1.0`.
- Addresses spanned dozens of /24 networks in several cloud regions.

Together these observations support **suspected sensor/honeypot contamination**. They supersede the earlier “firmware in cloud” interpretation. The public atlas records the aggregate research observations; the underlying host records are not exported. The network owner does not identify the operator of the suspected sensors.

For repeatable measurement, the catalog defines this explicit cloud-network cohort:

| Network context | ASN filter |
| --- | --- |
| Alibaba / Aliyun | AS37963, AS45102 |
| UCloud | AS135377 |
| Huawei cloud | AS55990, AS136907, AS58519 |

The network contexts were checked against Shodan organization facets on October 21. The union query includes both indexed ASN spellings, for example `asn:AS37963,37963,AS45102,45102,AS135377,135377,AS55990,55990,AS136907,136907,AS58519,58519`. Shodan returns some records with a numeric ASN and others with an `AS` prefix. The outside-cohort query applies six negative filters with both aliases, such as `-asn:AS37963,37963`. The first October 21 pass used only prefixed values; the later corrected snapshot includes the numeric aliases. Each query is intersected with the relevant component marker. A single union query avoids adding overlapping organization aliases.

The line inspector shows three worldwide measurements: raw matches, matches in these cloud networks, and matches outside them. Each has its own timestamp. Queries run independently against a changing index, so small differences between their totals are possible. The variant cards expose the queries, geography, ports, organizations and ASNs.

Cloud membership is a reproducible screening rule, not host-level verification. Results outside the cohort remain unclassified services; the earlier subtraction of roughly 74,000 cloud matches from 173,000 total matches is not a verified census of 99,000 physical devices. The wider ASN cohort and later measurements need not reproduce that organization-based estimate.

A separate RomPager/4.07 query measures the cloud cohort on **7547**, and another measures it on **9022**. This makes the contamination of those port slices visible. The small reported Aliyun contribution on 7547 does not establish that every remaining result is a real CPE, or that other datasets are free of sensors.

For mini_httpd the same ASN cohort is collected as a comparison. The RomPager banner sample does not classify the mini_httpd results as honeypots.

FOFA figures from earlier research used a different observation window and are not imported into these Shodan snapshots. The collector performs Count/facet requests only; it does not probe the indexed services.
