# Public research chronology

Edited English public edition, reviewed 10 October 2026. Section numbers preserve
references from project news. This is a publication-oriented account of the
research, with obsolete conclusions corrected and private security, operational
and host-level material omitted. The original research log is retained privately.
Historical numbers below are not current device counts. Use the dated atlas
responses for current query results.

<a id="section-1"></a>
## 1. Source-history review

The early easycwmp study compared public release tags and stable response markers; see [FINGERPRINTS.md](FINGERPRINTS.md). Realm and opaque patterns identify a component family but do not generally identify an exact release. Detailed unpublished behavior and security analysis are omitted.

<a id="section-2"></a>
## 2. Parser research

Private implementation analysis is outside this public edition. The atlas does not publish authentication-bypass, parser or reproduction details.

<a id="section-3"></a>
## 3. Active probe battery

The original lab work included active probes. Public response classes and the authorized historical scan are described in [FINGERPRINTS.md](FINGERPRINTS.md). The separate probe implementation is not distributed.

<a id="section-4"></a>
## 4. Scope of the public collector

The public collector queries Shodan aggregates only. It neither tests credentials nor sends requests to devices. Earlier authorized laboratory and operator measurements must not be confused with this workflow.

<a id="section-5"></a>
## 5. Research artifacts

Firmware extracts, raw exports, lab scripts, device addresses and operational logs are kept outside the public edition. The public tools are the Count collector, snapshot history, fact synchronizer and atlas builder.

<a id="section-6"></a>
## 6. Laboratory validation

Detailed results associated with unfinished disclosure remain private. A laboratory result does not automatically establish prevalence or exploitability across indexed devices.

<a id="section-7"></a>
## 7. Historical export analysis

The October 7 research export contained about 30k service records, including 20,502 relevant response banners and substantial full-text cloud noise. Structured header parsing omitted some authentication evidence, motivating a raw-response fallback in the private analyzer. Selection was not proven random. No host-level export is distributed.

<a id="section-8"></a>
## 8. Local test environment

The original pipeline was tested in an isolated lab. Its topology, operational commands and authentication tests are omitted. Current repository tests run offline and stub Shodan requests.

<a id="section-9.1"></a>
## 9.1. Realm-first discovery — October 7

Initial realm queries identified easycwmp (996,052 historical matches), icwmp (3,171,481), RDK-B (1,768,030) and IgdAuthentication (1,527,836). Counts represent the corresponding dated queries, not unique devices. The initial total was neither exhaustive nor disjoint.

<a id="section-9.2"></a>
## 9.2. Opaque-based expansion — October 7

Subtraction and clustering added ZTE, Sagemcom, Yapsie, ecntcwmp, Realtek, cwmpd, DT Speedport, ACSSimTool, gSOAP Service, leanoacs, Ruijie and miscellaneous realms. The easycwmp marker linked renamed forks. The early claim that DT and ACSSimTool share an SDK was later withdrawn: their shared opaque value is an RFC example.

<a id="section-9.3"></a>
## 9.3. Server-first classification — October 7

Server headers exposed populations missed by realm-only mining, including tr069 http server, gSOAP and TR069 Client. Port 30005 was shared by several families. Main-family and port-subset counts must not be added. Later source evidence refined the TR069 Client component hypothesis; it did not prove a single OEM.

<a id="section-9.4"></a>
## 9.4. Operator and port distributions — October 7

Historical facets associated icwmp with BT, tr069 http server with TPG/iiNet and WindTre, TR069 Client with Charter/Singtel/Maroc/EBOX, RDK-B with regional cable networks, and IgdAuthentication with STC/Play/Vivo. Ports 30005, 49501, 58603, 7170, 6264 and 1024/1025 showed why a single-port denominator misses relevant signatures. These are network associations, not hardware-model labels.

<a id="section-9.5"></a>
## 9.5. Basic authentication and ACS correction — October 7

Basic-marker mining found NettyServer and a small Huawei subset. The original inference that other HuaweiHomeGateway matches were mostly web interfaces was corrected by the October 10 response review. AVSystem libcwmp was reclassified as CPE software rather than ACS infrastructure. GenieACS, OpenACS and Axiros are separately labeled ACS-related lines. Only a subset of port 6264 matches belonged to Magticom/gSOAP.

<a id="section-9.6"></a>
## 9.6. Organization slices and missing HTTP evidence — October 7

Organization queries found additional Askey and MEiG patterns missed by opaque mining. Large Korean port-7547 populations lacked indexed HTTP signatures. Filtering is one possible explanation; the data do not establish a single cause or absence of TR-069.

<a id="section-9.7"></a>
## 9.7. US, Saudi, UK and Charter slices — October 7

Country and operator slices exposed multiple implementations within large networks. CPE-SERVER and Huawei became major registry lines; the earlier roughly 30k Huawei estimate was a Basic-only selection artifact. Bare 400/404 responses form a response class; their cause must not be assumed to be anti-scanning.

<a id="section-9.8"></a>
## 9.8. Numbering note

The original research log had no section 9.8. Existing references to subsequent section numbers are retained.

<a id="section-9.9"></a>
## 9.9. Monitoring and authentication research — October 7

An early per-query monitor introduced dated baselines and deltas. It is superseded for publication by tools/collect-map.py and timestamped snapshots. Detailed authentication research remains outside this release; see NONCE-PATHOLOGY.md for the interpretation boundary.

<a id="section-9.10"></a>
## 9.10. TR069 Client cross-service investigation — October 8

A 100-host research sample separated the common port-7547 pattern from Singtel auxiliary-port observations. Eighty-eight records exposed no useful neighboring vendor service. Earlier assertions of shared firmware were too strong because services could be observed days apart. Sercomm menu wording was naming evidence only. Later image checks and source comparisons are described in DEANON-TR069CLIENT.md.

<a id="section-9.11"></a>
## 9.11. Coverage review and missing lines — October 8

A 300-record HTTP-bearing development sample classified 70% of records and revealed a missing Sercomm-branded line. Other additions included Charter bare-404, DigAuth, CWMP-Agent, LANCOM and the Netcore/Netis CLI Server pattern. An Authentication token query was rejected as a substring artifact. This was coverage within a development sample, not a measured Internet-wide accuracy score.

<a id="section-9.12"></a>
## 9.12. Methodology corrections — October 8

Review corrected six important overclaims: RFC constants do not prove shared SDKs; ordinary Connection Request transport and response codes are not automatically defects; matches are not devices; asynchronous co-observations are not one firmware image; search-order downloads are not random; discovery queries are not necessarily exact classifiers. Count replaced search for aggregate-only collection. METHOD.md records these rules.

<a id="section-9.13"></a>
## 9.13. Operator drill-down — October 8

The first limited sweep collected top-country operator facets. It exposed BT across several components, Vodacom/ENS in the South African Sercomm slice, SFR in French tr069-http results, regional US IgdAuth networks and non-UK icwmp slices. Current collection expands this to every observed country–line pair and reports the remaining facet tail.

<a id="section-9.14"></a>
## 9.14. First interactive atlas — October 8

The initial map combined line, country and operator views with attribution badges, findings, overlaps and Shodan query links. All-port line totals can exceed a port-7547 denominator; the interface must state both scopes. Current entry points embed local geometry and require no runtime CDN.

<a id="section-9.15"></a>
## 9.15. Automated collection — October 8

The collector replaced ad hoc Count calls with a registry-driven pipeline, explicit denominators, operator slices, timestamps and collection status. The original limited runs are historical. The October 10 full refresh contains 52 lines, 2,457 pairs and 93 research queries, with no collection errors.

<a id="section-9.16"></a>
## 9.16. Private matcher regression work — October 8

A separate response-matcher package and banner corpus were used during development. That package carries a proprietary/confidential notice and is excluded from this publication. Its historical regression result is not a current guarantee of atlas classification accuracy.

<a id="section-9.17"></a>
## 9.17. Source and image attribution — October 8

Research found the CPE-SERVER string in an inspected ZTE H108N image and the tr069 http server string in an inspected TP-Link Archer VR1600v V2 image. DigAuth was linked to an Atheros openagent source template. These findings establish implementation evidence in those artifacts, not the OEM of every indexed match. Identical CWMP-Agent responses across Tunisia and Hong Kong supported a shared-component interpretation. Firmware and source extracts are not redistributed.

<a id="section-9.18"></a>
## 9.18. First Sercomm negative — October 8

The inspected RV6699 v4-RT image did not contain the main TR069 Client Server string or realm. A web-menu label used similar wording, which is not implementation evidence. This negative is limited to that image.

<a id="section-9.19"></a>
## 9.19. Second Sercomm negative — October 8

A second inspected RV6688v2-MTS image also lacked the main TR069 Client signature in the recovered material. The outcome weakens that particular carrier hypothesis but does not exclude unexamined models or regional builds. Extraction details are withheld from this public edition.

<a id="section-9.20"></a>
## 9.20. Companion signatures — October 8

Image/source research added the ZTE Mini web server companion line, a context-bounded fake-Apache/openagent pattern and TP-Link default-realm observations. Real Apache and concatenated honeypot banners can produce false positives. The companion web signatures are not Connection Request device counts.

<a id="section-9.21"></a>
## 9.21. Limits of artifact string mining — October 8

Further inspected artifacts yielded mostly configurable templates or generic strings rather than reliable new public signatures. This is a limit of the inspected material, not proof that all possible fingerprints have been exhausted.

<a id="section-9.22"></a>
## 9.22. Authentication implementation analysis — October 8

Detailed implementation analysis is withheld pending disclosure clearance. It is not reproduced in atlas metadata, translations or public collection plans.

<a id="section-9.23"></a>
## 9.23. Authentication sample follow-up — October 8

Detailed security conclusions are withheld. The Westell Secure realm remains a separately counted research query; a matching response format does not establish the underlying implementation or exploitability.

<a id="section-9.24"></a>
## 9.24. Explorer redesign — October 8

The map gained multi-select facets, a stable inspector, country/line comparisons, keyboard search, operator aggregation, exports, microstate markers and URL state. Focus, filters and map modes were reviewed together. Historical screenshots and local backup paths are not part of the public release.

<a id="section-9.25"></a>
## 9.25. Selection consistency — October 9

Country and line selection were aligned across map, tables and filters. Pointer handling, zoom, small-country rendering and operator-slice behavior were corrected. Known duplicate/superset lines were removed from the default sum, but the earlier label disjoint was too strong; complete disjointness is not proven.

<a id="section-9.26"></a>
## 9.26. Further interaction fixes — October 9

Region comparisons, observation cards, table stability, navigation offsets, labels and normalized operator rows were refined. Later review corrected operator coverage, denominators and missing-data behavior. Automated source-level checks complement browser testing.

<a id="section-9.27"></a>
## 9.27. Integrator references and Starlink control — October 10

The research log recorded easycwmp source/package references in several integrator ecosystems, including Teltonika, Banana Pi, Wallystech and OpenWrt derivatives. Inclusion in a source tree does not prove shipping configuration. One inspected Starlink source release contained inherited package material while its build configuration disabled the package. A SpaceX organization query is a network slice and cannot identify Starlink-manufactured routers. The easycwmp-family SpaceX control returned zero in the current snapshot; this does not prove global absence.

<a id="section-9.28"></a>
## 9.28. Observation and variant layer — October 10

Additional exact queries cover family markers, Google Fiber/Fidium slices, ZTE companion web/telnet signatures, Huawei auxiliary ports, TR069 Client operators, TP-Link realms, IgdAuth ports, GenieACS versions, DigAuth, CWMP-Agent and Sercomm country slices. The layer now has 39 dated observations. Old prose counts are historical. A GenieACS version label is not a vulnerability verdict.

<a id="section-9.29"></a>
## 9.29. Four interface languages — October 10

English, Spanish, Chinese and Russian share the same data and selection model. Language choice can be encoded in the URL and stored locally. Country names use locale-aware display names. Translation fallback and template-expression errors were corrected.

<a id="section-9.30"></a>
## 9.30. Full refresh and publication review — October 10

The completed snapshot-20261010-102121 contains 52 lines, 2,457 operator pairs and 93 variants. All 39 observation queries are covered; 35 source counts changed during synchronization. Fresh full runs update facts atomically and preserve original research counts. Public source links, English documentation and a clean release candidate were prepared. The owner approved fingerprint research for publication under Apache 2.0; new vulnerability findings and the separate probes package remain excluded.

## Additional bounded negative: SOAP namespace prefix

The inspected gSOAP 2.7 and 2.8 laboratory responses used the same SOAP-ENV prefix. This did not validate a version discriminator; vendor or client variation cannot be inferred from that check alone.

<a id="section-9.31"></a>
## 9.31. Second-image evidence for the ZTE and Huawei lines — October 12

Inspection of a ZTE F670L image pair (two firmware generations) found the
`cpe@zte.com` connection-request realm and a default listener port of 58000
in both generations. This extends the implementation evidence for the ZTE
line beyond the previously inspected H108N image to a newer GPON platform;
it does not attribute every indexed match to that platform. Operator NAT can
hide connection-request listeners from public indexing; the visible line
cannot measure the total deployment of this generation.

A Huawei HG8145V5 image independently confirms a connection-request listener
default of port 30005 and a nonce path reading from the operating-system
random device, consistent with the observed response uniqueness
(see [DEANON-HUAWEI-CR.md](DEANON-HUAWEI-CR.md)). Security evaluation of
these images is not part of the public release.

<a id="section-9.32"></a>
## 9.32. FreeACS admin-UI line — October 12

A title-based query (`http.title:"FreeACS"`) measures six open admin
interfaces: two on Italian ISP networks (Fastweb, BBANDA), two on a Singapore
DigitalOcean host, one on Google Cloud and one on Oracle Cloud. All six serve
the stock FreeACS login page. The records carry deployment-coherent variance
rather than honeypot markers: direct-Tomcat responses (Apache-Coyote, classic
JSESSIONID) on the ISP hosts versus nginx reverse-proxy responses with
sticky-session JSESSIONID prefixes on the cloud hosts, and one ISP pair shows
a doubled "Web Web" module-name artifact in the title. The sample is small
and one record dates to mid-September; no honeypot markers were identified
in the inspected records. The count is an admin-UI
lower bound: the SOAP and TR-069 modules expose no title or banner.

<a id="section-9.33"></a>
## 9.33. TR069 Client attributed to Works Systems OneAgent TR — October 13

The main TR069 Client family is identified as Works
Systems' embeddable OneAgent TR client. Evidence: the full 401 template with
the exact Server string and Digest parameter order found inside `tr_agent`
of a public Nokia FastMile 5G Gateway 3.2 dump (which also carries Workssys
strings), Works Systems copyright plus an explicit OneAgent-TR build label
in ASUS asuswrt `apps/private/tr069`, and Works Systems copyright in the
Atheros AthSDK openagent-2.0 source that the earlier source-lineage work had
already tied to this family. OneAgent TR was documented as a component
licensed across xDSL/cable/xPON/Wi-Fi platforms, which explains a
byte-identical banner across unrelated operators. Consequences recorded in
the registry: the full Server value is the primary marker; qop presence is a
build variant; the hardware OEM is not derivable from the response. The
sub-family guide and bounded negatives remain valid as search history.
Pinned public sources, binary hashes and template offsets are recorded in
[the attribution dossier](DEANON-TR069CLIENT.md#public-evidence).

<a id="section-9.34"></a>
## 9.34. Software-lineage attribution — October 13

Two disassembly passes closed attribution questions. The older inspected ZTE
generation's connection-request handler is one code family with the newer
platform's (same challenge template literals; the visible fleet's banner
matches the inspected binary's format string). The inspected TP-Link handler
carries the Works Systems openagent software lineage — its function names and
response template match the published GPL source. Nonce-generation mechanics
belong to the restricted census and are withheld from the public release pending
disclosure. At that review, IgdAuthentication remained unattributed; the subsequent
public binary evidence is recorded in section 9.41.

<a id="section-9.35"></a>
## 9.35. CLI deployment and active fingerprint observations — October 13

Three observations extend the public fingerprint record:

- **OneAgent CLI handler deployment facts.** The companion `TR069 client CLI
  Server` line has 1,855 matches in the [October 10 snapshot](data/mapdata/snapshot-20261010-102121/tr069-client-cli-server-netcore.json),
  all on the component's compiled-default port 1234. AS17306 accounts for
  1,045 matches after combining Shodan's `as17306` and `17306` buckets.
  Country totals include the United States (1,082), China (564), Serbia
  (137), Iran (15), Mexico (15) and Australia (10). The Serbian ASN buckets
  normalize to AS8400, Telekom Srbija, with 137 matches. The [October 12
  snapshot](data/mapdata/snapshot-20261012-145337/tr069-client-cli-server-netcore.json)
  records 1,850 matches, again all on 1234. Port observations alone do not
  establish which configuration settings operators changed.
- **CLI route-set build classes.** Sampled CLI deployments in China and
  Serbia expose a fuller route table than the sampled United States
  fixed-wireless deployments. Route presence provides a build discriminator
  for the inspected endpoints. The sample does not establish country-wide
  build classes; route names and security findings remain outside this note.
- **Active response classes for easycwmp.** Closing the TCP write side before
  sending request bytes distinguishes two upstream reference handlers: 1.6.2
  closes without an HTTP response; 1.7.0 returns 409. A 401 response alone
  does not establish an older release, and no response does not establish
  filtering. A 200 response needs separate interpretation before making any
  authentication claim. The [fingerprint note](FINGERPRINTS.md#easycwmp-source-comparison)
  links the source comparison and retains the historical scan as response
  counts. Shodan banners cannot reproduce this controlled active experiment.

<a id="section-9.36"></a>
## 9.36. Cross-index observations (FOFA) — October 13

A second index supplied 13 signature aggregates and 22 country slices on port
7547. The [public comparison](CROSS-INDEX.md#method) retains them as an
independent dated source. Exact FOFA retrieval timestamps and retention filters
were not saved; query notation comes from the research summary. The atlas pairs
these values with its saved October 13 Shodan snapshot, without combining totals
or interpreting their ratios as measured coverage.

Research follow-ups include the Gateway realm in UK:1024 and Canada:10001
operator contexts and DSLForum CPE Management in DE:7170 and SG/GB:8085 contexts.
They justify separate catalog queries. A shared realm does not resolve the
component supplier, and index product labels do not supply independent proof.

<a id="section-9.37"></a>
## 9.37. Vendor dynamic-DNS names crossed with TR-069 ports — October 13

Some router platforms publish their services under vendor-operated dynamic
names (optionally relaying through the vendor cloud for addresses behind
CGNAT). Cross-referencing those name spaces with TR-069 ports in the second
engine gives a small but real discovery surface: a few hundred to ~1.5k
hosts per vendor name space carry an open 7547, including at least one
exact vendor-pair match (a vendor DDNS name on that vendor's own TR-069
server string). Two limits are recorded from the same measurement: dynamic
addresses make name-to-device mappings stale (a vendor name was observed on
a clearly different vendor's device), and no vendor dynamic-DNS names were found in the inspected anonymous-line
samples. Those samples offered no positive attribution evidence from DDNS.
Cloud-relayed services require separate observation: inbound port scans do not
by themselves enumerate devices behind CGNAT.

<a id="section-9.38"></a>
## 9.38. Korean authentication-marker coverage — October 13

The research records 4,707,708 FOFA matches on port 7547 in South Korea, with
157,484 in its authentication-header subset (about 3.35%). This measures indexed
`WWW-Authenticate` presence. The complement is not a measured population of
silent devices: missing headers can reflect response behavior, scanning or
indexing. These counts do not test geo-filtering or establish device-side policy.
A separate port-7548 query returned 7,413 matches. See the
[cross-index follow-ups](CROSS-INDEX.md#follow-ups).

<a id="section-9.39"></a>
## 9.39. China-labeled aggregate and port reuse — October 13

The research summary records 5,902,772 FOFA matches on port 7547 under its CN
label and 396,785 authentication-marker matches. Operator examples include
Taiwan; country assignments require normalization before this row can enter the
country comparison. Sampled non-TR-069 services show that the port is reused.
The sample does not measure their prevalence in the remaining millions of
records. Neither the port total nor the authentication-header subset establishes
a protocol population.

<a id="section-9.40"></a>
## 9.40. Twenty-two country slices — October 13

The [comparison dataset](data/index-comparison.json) records FOFA port-7547
aggregates for 22 countries and the corresponding saved Shodan country facets.
Differences are useful leads for follow-up sampling. Different collection windows,
queries and scan footprints prevent interpreting the ratios as coverage
multipliers or revising a global device ranking. Authentication-marker presence
is an additional observation, not a complete TR-069 classifier.

<a id="section-9.41"></a>
## 9.41. IgdAuthentication attributed to Broadcom CMS tr69c — October 14

The component attribution is supported by a public ZyXEL VMG1312-B10A client
binary: its realm, challenge parameter order and distinctive fixed opaque
marker match the observed family. The
[public dossier](DEANON-IGDAUTH.md#public-evidence), independently checked on
October 15, supplies a pinned source, SHA-256, file size and string offsets.
The attribution identifies a component lineage, not every hardware OEM.
The October 13 Shodan record remains 1,540,730 query matches.

The DSLForum-realm family has a different response template and retains an
unresolved supplier. The atlas now calls it DSLForum CPE Management, preserving
its stable ID and historical measurements. Operator/port follow-ups are recorded
in [FINGERPRINTS.md](FINGERPRINTS.md#dslforum-cpe-management).

<a id="section-9.44"></a>
## 9.44. Broadcom SDK across management and Wi-Fi interfaces — November 1

Quentin Kaiser's public [WPSplinter catalog](https://github.com/qkaiser/broadcom-wps/blob/039b1514e063f71b671531606b2d33a1eb3bb6eb/README.md#affected-devices)
provides model, firmware and operator references for Broadcom-based CPE.
TRON-069 uses these references to compare software platforms and choose
firmware for attribution research.

The inspected ZyXEL C1000Z and C1100Z trees contain the attributed Broadcom
CMS tr69c client alongside Broadcom WPS Monitor. The reported static-rule
matches add an independent component-identification signal. The observed
relationship is between TR-069 connection-request and Wi-Fi components in
these firmware trees; Shodan measurements remain counts of CR-query matches.

The catalog also lists Askey TCG3000 for Orange Belgium/VOO, RTF3505VW for
Movistar/Telefónica, and Speedport W 723V Typ A (RTV1645VW-E83) for Deutsche
Telekom. These are external model/operator references. Askey is a firmware
research lead for the unresolved DSLForum response class. Attribution still
requires the exact realm and response template in a sourced CR binary;
operator overlap or WPS component identification alone does not establish it.

Public cards describe software composition and evidence scope. Binary-level
rule results and operational material remain outside this repository; the
atlas does not assign vulnerability status to models, operators or map points.
