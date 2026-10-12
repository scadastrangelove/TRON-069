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
