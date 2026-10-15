# TR-069 / CWMP signature registry

Public edition, 15 October 2026. This table uses snapshot-20261015-201645. Counts are exact query matches, not unique devices. Rows and variants overlap. Dedicated ACS lines are distinguished from CPE; mixed and unknown roles remain explicit.

The attribution badge describes evidence about the signature/component. A source or image match does not identify every device model or establish vulnerability. See [METHOD.md](METHOD.md) and [research coverage](data/research-findings.json).

| Line | Role | Query matches | Collected (UTC) | Query | Evidence |
| --- | --- | ---: | --- | --- | --- |
| <a id="cpe-server-1-0"></a>CPE-SERVER/1.0 | cpe | 3,557,329 | 2026-10-15T20:17:25+00:00 | `"CPE-SERVER/1.0"` | [proven](NOTES.md) |
| <a id="icwmp-iopsys"></a>icwmp (iopsys) | cpe | 3,241,868 | 2026-10-15T20:16:47+00:00 | `"authenticate@cwmp"` | [proven](NOTES.md) |
| <a id="huaweihomegateway"></a>HuaweiHomeGateway | cpe | 2,931,130 | 2026-10-15T20:16:55+00:00 | `"HuaweiHomeGateway"` | [proven](DEANON-HUAWEI-CR.md) |
| <a id="huaweihomegateway-cr-slice"></a>HuaweiHomeGateway CR slice | cpe | 2,705,645 | 2026-10-15T20:17:26+00:00 | `port:7547 "HuaweiHomeGateway"` | [proven](DEANON-HUAWEI-CR.md) |
| <a id="tr069-http-server"></a>tr069 http server | cpe | 1,993,969 | 2026-10-15T20:16:48+00:00 | `"tr069 http server"` | [proven](NOTES.md) |
| <a id="gsoap-park"></a>gSOAP park | mixed | 1,869,220 | 2026-10-15T20:16:49+00:00 | `"Server: gSOAP"` | [hypothesis](NOTES.md) |
| <a id="rdk-b-ccsptr069pa"></a>RDK-B CcspTr069Pa | cpe | 1,840,025 | 2026-10-15T20:16:50+00:00 | `"Cisco_CCSP_CWMP_TCPCR"` | [proven](NOTES.md) |
| <a id="tr069-client"></a>TR069 Client | cpe | 1,691,379 | 2026-10-15T20:16:52+00:00 | `"TR069 client TCP connection request Server"` | [Works Systems OneAgent TR (binary-proven)](DEANON-TR069CLIENT.md) |
| <a id="igdauthentication"></a>IgdAuthentication | cpe | 1,589,284 | 2026-10-15T20:16:53+00:00 | `"IgdAuthentication"` | [Broadcom CMS tr69c (binary-proven)](DEANON-IGDAUTH.md) |
| <a id="gsoap-2-7-vendor-map"></a>gSOAP/2.7 vendor map | mixed | 1,238,723 | 2026-10-15T20:17:35+00:00 | `port:7547 "Server: gSOAP/2.7"` | [class](NOTES.md) |
| <a id="easycwmp-vanilla"></a>easycwmp vanilla | cpe | 1,020,333 | 2026-10-15T20:16:54+00:00 | `"realm@easycwmp"` | [proven](NOTES.md) |
| <a id="askeycwmp-askey"></a>ASKEYCWMP (Askey) | cpe | 687,899 | 2026-10-15T20:17:19+00:00 | `port:7547 ASKEYCWMP` | [proven](NOTES.md) |
| <a id="centurylink-lighttpd"></a>CenturyLink lighttpd | cpe | 449,312 | 2026-10-15T20:17:27+00:00 | `port:7547 country:US lighttpd` | [hypothesis](NOTES.md) |
| <a id="sercomm-cpe-authentication"></a>Sercomm CPE Authentication | cpe | 314,568 | 2026-10-15T20:17:37+00:00 | `"Sercomm CPE Authentication"` | [proven](NOTES.md) |
| <a id="windtre-tr069-http-server"></a>WindTre tr069-http-server | cpe | 278,220 | 2026-10-15T20:17:33+00:00 | `port:7547 country:IT "tr069 http server"` | [class](NOTES.md) |
| <a id="zte"></a>ZTE | cpe | 261,847 | 2026-10-15T20:16:57+00:00 | `"cpe@zte.com"` | [proven](NOTES.md) |
| <a id="sagemcom"></a>Sagemcom | cpe | 219,983 | 2026-10-15T20:16:56+00:00 | `"Sagemcom TR-069"` | [proven](NOTES.md) |
| <a id="dt-speedport-sdk"></a>DSLForum CPE Management | cpe | 120,347 | 2026-10-15T20:17:04+00:00 | `"DSLForum CPE Management"` | [response class; supplier unresolved](FINGERPRINTS.md#dslforum-cpe-management) |
| <a id="gsoap-2-8-vendor-map"></a>gSOAP/2.8 vendor map | mixed | 106,562 | 2026-10-15T20:17:35+00:00 | `port:7547 "Server: gSOAP/2.8"` | [class](NOTES.md) |
| <a id="charter-anti-scan-404"></a>Charter anti-scan 404 | unknown | 112,359 | 2026-10-15T20:17:38+00:00 | `port:7547 "HTTP/1.1 404" org:"Charter Communications"` | [class](NOTES.md) |
| <a id="cwmp-server"></a>cwmp server | unknown | 85,556 | 2026-10-15T20:17:47+00:00 | `"Server: cwmp server"` | [anonymous](ACS-HUNT.md) |
| <a id="mini-web-server-1-0-zte-corp"></a>Mini web server 1.0 ZTE corp | cpe | 77,499 | 2026-10-15T20:17:44+00:00 | `"Mini web server 1.0 ZTE corp"` | [proven](NOTES.md) |
| <a id="yapsieworld"></a>YapsieWorld | cpe | 72,461 | 2026-10-15T20:16:59+00:00 | `"YapsieWorld"` | [anonymous](NOTES.md) |
| <a id="sky-ee-tr069-http-server"></a>Sky/EE tr069-http-server | cpe | 61,502 | 2026-10-15T20:17:29+00:00 | `port:7547 country:GB "tr069 http server"` | [class](NOTES.md) |
| <a id="easycwmp-fork-ecntcwmp"></a>easycwmp fork: ecntcwmp | cpe | 62,024 | 2026-10-15T20:17:08+00:00 | `"realm@ecntcwmp"` | [proven](NOTES.md) |
| <a id="gateway-realm"></a>Gateway realm | cpe | 35,308 | 2026-10-15T20:17:31+00:00 | `port:7170 realm="Gateway"` | [anonymous](ACS-HUNT.md) |
| <a id="ti-cpe-authentication"></a>TI CPE Authentication | cpe | 32,112 | 2026-10-15T20:17:30+00:00 | `"TI CPE Authentication"` | [proven](NOTES.md) |
| <a id="decimal-nonce-class"></a>decimal-nonce class | unknown | 25,383 | 2026-10-15T20:17:46+00:00 | `port:7547 "algorithm=\"MD5\",qop=\"auth\"" "nonce=\"17"` | [class](NOTES.md) |
| <a id="nettyserver"></a>NettyServer | cpe | 30,262 | 2026-10-15T20:17:14+00:00 | `"NettyServer" port:7547` | [hypothesis](ACS-HUNT.md) |
| <a id="digauth"></a>DigAuth | cpe | 29,631 | 2026-10-15T20:16:58+00:00 | `"DigAuth"` | [proven](DEANON-TR069CLIENT.md) |
| <a id="realtek-sdk"></a>Realtek SDK | cpe | 28,886 | 2026-10-15T20:17:01+00:00 | `"realtek.com.tw"` | [proven](NOTES.md) |
| <a id="magticom-gsoap"></a>Magticom gSOAP | cpe | 27,179 | 2026-10-15T20:17:00+00:00 | `port:6264 gSOAP` | [proven](NOTES.md) |
| <a id="kt-cems"></a>KT CEMS | cpe | 25,669 | 2026-10-15T20:17:23+00:00 | `"ktcems.com"` | [proven](NOTES.md) |
| <a id="qacafe-cdrouter-test-realm"></a>qacafe (CDRouter test realm) | cpe | 21,688 | 2026-10-15T20:17:24+00:00 | `"qacafe"` | [proven](NOTES.md) |
| <a id="cwmpd-tr069agent"></a>cwmpd / TR069Agent | cpe | 19,105 | 2026-10-15T20:17:03+00:00 | `"cwmpd" opaque` | [proven](NOTES.md) |
| <a id="cwmp-agent-orange-tunisie"></a>CWMP-Agent (Orange Tunisie) | cpe | 19,987 | 2026-10-15T20:17:39+00:00 | `"CWMP-Agent"` | [proven](NOTES.md) |
| <a id="acssimtool"></a>ACSSimTool | cpe | 11,241 | 2026-10-15T20:17:05+00:00 | `"ACSSimTool"` | [class](ACS-HUNT.md) |
| <a id="arris-cpe-authentication"></a>Arris CPE Authentication | cpe | 9,437 | 2026-10-15T20:17:28+00:00 | `"Arris CPE Authentication"` | [proven](NOTES.md) |
| <a id="gsoap-service-realm"></a>gSOAP Service realm | cpe | 6,847 | 2026-10-15T20:17:07+00:00 | `port:7547 opaque "gSOAP Service"` | [class](NOTES.md) |
| <a id="cwmp-lancom"></a>CWMP@Lancom | cpe | 6,434 | 2026-10-15T20:17:40+00:00 | `port:7547 "CWMP@Lancom"` | [proven](NOTES.md) |
| <a id="avsystem-libcwmp"></a>avsystem-libcwmp | cpe | 6,524 | 2026-10-15T20:17:06+00:00 | `"avsystem-libcwmp"` | [proven](ACS-HUNT.md) |
| <a id="easycwmp-fork-leanoacs"></a>easycwmp fork: leanoacs | cpe | 4,335 | 2026-10-15T20:17:10+00:00 | `"realm@leanoacs"` | [proven](NOTES.md) |
| <a id="junk-realms"></a>junk realms | unknown | 3,816 | 2026-10-15T20:17:12+00:00 | `port:7547 opaque "dirname"` | [class](NOTES.md) |
| <a id="genieacs-admin-ui"></a>GenieACS admin-UI | acs | 3,903 | 2026-10-15T20:17:15+00:00 | `http.title:"GenieACS"` | [proven](NOTES.md) |
| <a id="fake-apache-openagent"></a>fake-Apache openagent | cpe | 3,035 | 2026-10-15T20:17:45+00:00 | `port:7547 "Apache/2.0.40 (Red Hat Linux)"` | [proven](DEANON-TR069CLIENT.md) |
| <a id="meig-meigsmart-com"></a>MEiG (meigsmart.com) | cpe | 2,647 | 2026-10-15T20:17:22+00:00 | `"www.meigsmart.com"` | [proven](NOTES.md) |
| <a id="tr069-client-cli-server-netcore"></a>TR069 client CLI Server (Netcore) | cpe | 1,874 | 2026-10-15T20:17:41+00:00 | `"TR069 client CLI Server"` | [proven](DEANON-TR069CLIENT.md) |
| <a id="telefonica-cwmpweb"></a>Telefónica cwmpWeb | acs | 1,300 | 2026-10-15T20:17:48+00:00 | `"cwmpWeb" "main.acs.telefonica.net"` | [proven](ACS-HUNT.md) |
| <a id="ruijie-cpe"></a>RUIJIE-CPE | cpe | 527 | 2026-10-15T20:17:11+00:00 | `"RUIJIE-CPE"` | [proven](NOTES.md) |
| <a id="easycwmp-fork-ltecpe"></a>easycwmp fork: ltecpe | cpe | 82 | 2026-10-15T20:17:10+00:00 | `"realm@ltecpe"` | [proven](NOTES.md) |
| <a id="openacs"></a>openacs | acs | 15 | 2026-10-15T20:17:16+00:00 | `"openacs"` | [proven](NOTES.md) |
| <a id="axiros"></a>Axiros | acs | 8 | 2026-10-15T20:17:17+00:00 | `"Axiros"` | [proven](NOTES.md) |
| <a id="freeacs"></a>FreeACS Web | acs | 6 | 2026-10-15T20:17:19+00:00 | `http.title:"FreeACS"` | [title signature; public reports](PUBLIC-DISCLOSURES.md#freeacs-20261012) |

## Scope and historical corrections

Huawei auxiliary ports are authentication-service slices, not automatically web interfaces. TR069 Client is Works Systems OneAgent TR; DigAuth and fake-Apache trace to the earlier Works Systems openagent branch. Device OEM attribution remains separate. Gateway/TIM vendor attribution remains open. NettyServer/WindTre remains a platform hypothesis. The shared DT/ACSSimTool RFC-example constant is not proof of a shared SDK. AVSystem libcwmp is CPE software; Telefónica cwmpWeb is an ACS frontend.

The original October 8 development sample classified 70% of 300 HTTP-bearing records. This is neither fleet-wide precision nor a current coverage measurement. Known overlaps are excluded from the default sum, but full disjointness is unproven.

Editorial attribution review: 15 October 2026. IgdAuthentication maps to Broadcom CMS tr69c through a public binary anchor. DSLForum CPE Management keeps ID `dt-speedport-sdk`; no measurements were relabeled with a new collection date. The [FOFA comparison](CROSS-INDEX.md) is separate from this Shodan registry.
