# TR-069 / CWMP signature registry

Public edition, 1 November 2026. This table uses the full snapshot-20261101-091700. Counts are exact query matches, not unique devices. Rows and variants overlap. Dedicated ACS lines are distinguished from CPE; mixed and unknown roles remain explicit.

The attribution badge describes evidence about the signature/component. A source or image match does not identify every device model or establish vulnerability. See [METHOD.md](METHOD.md) and [research coverage](data/research-findings.json).

| Line | Role | Query matches | Collected (UTC) | Query | Evidence |
| --- | --- | ---: | --- | --- | --- |
| <a id="cpe-server-1-0"></a>CPE-SERVER/1.0 | cpe | 3,964,632 | 2026-11-01T09:17:40+00:00 | `"CPE-SERVER/1.0"` | [proven](NOTES.md) |
| <a id="icwmp-iopsys"></a>icwmp (iopsys) | cpe | 3,556,465 | 2026-11-01T09:17:02+00:00 | `"authenticate@cwmp"` | [proven](NOTES.md) |
| <a id="huaweihomegateway"></a>HuaweiHomeGateway | cpe | 3,149,908 | 2026-11-01T09:17:10+00:00 | `"HuaweiHomeGateway"` | [proven](DEANON-HUAWEI-CR.md) |
| <a id="huaweihomegateway-cr-slice"></a>HuaweiHomeGateway CR slice | cpe | 2,900,740 | 2026-11-01T09:17:40+00:00 | `port:7547 "HuaweiHomeGateway"` | [proven](DEANON-HUAWEI-CR.md) |
| <a id="tr069-http-server"></a>tr069 http server | cpe | 2,152,515 | 2026-11-01T09:17:03+00:00 | `"tr069 http server"` | [proven](NOTES.md) |
| <a id="gsoap-park"></a>gSOAP park | mixed | 2,016,946 | 2026-11-01T09:17:04+00:00 | `"Server: gSOAP"` | [hypothesis](NOTES.md) |
| <a id="rdk-b-ccsptr069pa"></a>RDK-B CcspTr069Pa | cpe | 1,941,673 | 2026-11-01T09:17:05+00:00 | `"Cisco_CCSP_CWMP_TCPCR"` | [proven](NOTES.md) |
| <a id="tr069-client"></a>TR069 Client | cpe | 1,785,081 | 2026-11-01T09:17:07+00:00 | `"TR069 client TCP connection request Server"` | [Works Systems OneAgent TR (binary-proven)](DEANON-TR069CLIENT.md) |
| <a id="igdauthentication"></a>IgdAuthentication | cpe | 1,764,489 | 2026-11-01T09:17:08+00:00 | `"IgdAuthentication"` | [Broadcom CMS tr69c (binary-proven)](DEANON-IGDAUTH.md) |
| <a id="gsoap-2-7-vendor-map"></a>gSOAP/2.7 vendor map | mixed | 1,302,495 | 2026-11-01T09:17:48+00:00 | `port:7547 "Server: gSOAP/2.7"` | [class](NOTES.md) |
| <a id="easycwmp-vanilla"></a>easycwmp vanilla | cpe | 1,084,316 | 2026-11-01T09:17:09+00:00 | `"realm@easycwmp"` | [proven](NOTES.md) |
| <a id="askeycwmp-askey"></a>ASKEYCWMP (Askey) | cpe | 782,930 | 2026-11-01T09:17:34+00:00 | `port:7547 ASKEYCWMP` | [proven](NOTES.md) |
| <a id="centurylink-lighttpd"></a>CenturyLink lighttpd | cpe | 454,464 | 2026-11-01T09:17:41+00:00 | `port:7547 country:US lighttpd` | [hypothesis](NOTES.md) |
| <a id="sercomm-cpe-authentication"></a>Sercomm CPE Authentication | cpe | 331,630 | 2026-11-01T09:17:50+00:00 | `"Sercomm CPE Authentication"` | [proven](NOTES.md) |
| <a id="windtre-tr069-http-server"></a>WindTre tr069-http-server | cpe | 298,363 | 2026-11-01T09:17:47+00:00 | `port:7547 country:IT "tr069 http server"` | [class](NOTES.md) |
| <a id="zte"></a>ZTE | cpe | 280,196 | 2026-11-01T09:17:13+00:00 | `"cpe@zte.com"` | [proven](NOTES.md) |
| <a id="sagemcom"></a>Sagemcom | cpe | 218,991 | 2026-11-01T09:17:11+00:00 | `"Sagemcom TR-069"` | [proven](NOTES.md) |
| <a id="dt-speedport-sdk"></a>DSLForum CPE Management | cpe | 129,183 | 2026-11-01T09:17:19+00:00 | `"DSLForum CPE Management"` | [response class; supplier unresolved](FINGERPRINTS.md#dslforum-cpe-management) |
| <a id="gsoap-2-8-vendor-map"></a>gSOAP/2.8 vendor map | mixed | 110,417 | 2026-11-01T09:17:49+00:00 | `port:7547 "Server: gSOAP/2.8"` | [class](NOTES.md) |
| <a id="charter-anti-scan-404"></a>Charter anti-scan 404 | unknown | 124,036 | 2026-11-01T09:17:51+00:00 | `port:7547 "HTTP/1.1 404" org:"Charter Communications"` | [class](NOTES.md) |
| <a id="cwmp-server"></a>cwmp server | unknown | 90,199 | 2026-11-01T09:17:59+00:00 | `"Server: cwmp server"` | [anonymous](ACS-HUNT.md) |
| <a id="mini-web-server-1-0-zte-corp"></a>Mini web server 1.0 ZTE corp | cpe | 111,786 | 2026-11-01T09:17:56+00:00 | `"Mini web server 1.0 ZTE corp"` | [proven](NOTES.md) |
| <a id="yapsieworld"></a>YapsieWorld | cpe | 76,857 | 2026-11-01T09:17:15+00:00 | `"YapsieWorld"` | [anonymous](NOTES.md) |
| <a id="sky-ee-tr069-http-server"></a>Sky/EE tr069-http-server | cpe | 68,470 | 2026-11-01T09:17:44+00:00 | `port:7547 country:GB "tr069 http server"` | [class](NOTES.md) |
| <a id="easycwmp-fork-ecntcwmp"></a>easycwmp fork: ecntcwmp | cpe | 68,877 | 2026-11-01T09:17:23+00:00 | `"realm@ecntcwmp"` | [proven](NOTES.md) |
| <a id="gateway-realm"></a>Gateway realm | cpe | 44,477 | 2026-11-01T09:17:46+00:00 | `port:7170 realm="Gateway"` | [anonymous](ACS-HUNT.md) |
| <a id="ti-cpe-authentication"></a>TI CPE Authentication | cpe | 40,508 | 2026-11-01T09:17:45+00:00 | `"TI CPE Authentication"` | [proven](NOTES.md) |
| <a id="decimal-nonce-class"></a>decimal-nonce class | unknown | 30,065 | 2026-11-01T09:17:58+00:00 | `port:7547 "algorithm=\"MD5\",qop=\"auth\"" "nonce=\"17"` | [class](NOTES.md) |
| <a id="nettyserver"></a>NettyServer | cpe | 36,747 | 2026-11-01T09:17:29+00:00 | `"NettyServer" port:7547` | [hypothesis](ACS-HUNT.md) |
| <a id="digauth"></a>DigAuth | cpe | 27,431 | 2026-11-01T09:17:14+00:00 | `"DigAuth"` | [proven](DEANON-TR069CLIENT.md) |
| <a id="realtek-sdk"></a>Realtek SDK | cpe | 31,153 | 2026-11-01T09:17:17+00:00 | `"realtek.com.tw"` | [proven](NOTES.md) |
| <a id="magticom-gsoap"></a>Magticom gSOAP | cpe | 30,273 | 2026-11-01T09:17:16+00:00 | `port:6264 gSOAP` | [proven](NOTES.md) |
| <a id="kt-cems"></a>KT CEMS | cpe | 25,961 | 2026-11-01T09:17:37+00:00 | `"ktcems.com"` | [proven](NOTES.md) |
| <a id="qacafe-cdrouter-test-realm"></a>qacafe (CDRouter test realm) | cpe | 22,770 | 2026-11-01T09:17:38+00:00 | `"qacafe"` | [proven](NOTES.md) |
| <a id="cwmpd-tr069agent"></a>cwmpd / TR069Agent | cpe | 22,076 | 2026-11-01T09:17:18+00:00 | `"cwmpd" opaque` | [proven](NOTES.md) |
| <a id="cwmp-agent-orange-tunisie"></a>CWMP-Agent (Orange Tunisie) | cpe | 23,555 | 2026-11-01T09:17:52+00:00 | `"CWMP-Agent"` | [proven](NOTES.md) |
| <a id="acssimtool"></a>ACSSimTool | cpe | 11,072 | 2026-11-01T09:17:20+00:00 | `"ACSSimTool"` | [class](ACS-HUNT.md) |
| <a id="arris-cpe-authentication"></a>Arris CPE Authentication | cpe | 8,743 | 2026-11-01T09:17:43+00:00 | `"Arris CPE Authentication"` | [proven](NOTES.md) |
| <a id="gsoap-service-realm"></a>gSOAP Service realm | cpe | 7,569 | 2026-11-01T09:17:22+00:00 | `port:7547 opaque "gSOAP Service"` | [class](NOTES.md) |
| <a id="cwmp-lancom"></a>CWMP@Lancom | cpe | 6,544 | 2026-11-01T09:17:53+00:00 | `port:7547 "CWMP@Lancom"` | [proven](NOTES.md) |
| <a id="avsystem-libcwmp"></a>avsystem-libcwmp | cpe | 6,502 | 2026-11-01T09:17:21+00:00 | `"avsystem-libcwmp"` | [proven](ACS-HUNT.md) |
| <a id="easycwmp-fork-leanoacs"></a>easycwmp fork: leanoacs | cpe | 4,592 | 2026-11-01T09:17:24+00:00 | `"realm@leanoacs"` | [proven](NOTES.md) |
| <a id="junk-realms"></a>junk realms | unknown | 4,131 | 2026-11-01T09:17:28+00:00 | `port:7547 opaque "dirname"` | [class](NOTES.md) |
| <a id="genieacs-admin-ui"></a>GenieACS admin-UI | acs | 4,294 | 2026-11-01T09:17:30+00:00 | `http.title:"GenieACS"` | [proven](NOTES.md) |
| <a id="fake-apache-openagent"></a>fake-Apache openagent | cpe | 3,149 | 2026-11-01T09:17:57+00:00 | `port:7547 "Apache/2.0.40 (Red Hat Linux)"` | [proven](DEANON-TR069CLIENT.md) |
| <a id="meig-meigsmart-com"></a>MEiG (meigsmart.com) | cpe | 3,002 | 2026-11-01T09:17:35+00:00 | `"www.meigsmart.com"` | [proven](NOTES.md) |
| <a id="tr069-client-cli-server-netcore"></a>TR069 client CLI Server (Netcore) | cpe | 1,830 | 2026-11-01T09:17:54+00:00 | `"TR069 client CLI Server"` | [proven](DEANON-TR069CLIENT.md) |
| <a id="telefonica-cwmpweb"></a>Telefónica cwmpWeb | acs | 635 | 2026-11-01T09:18:00+00:00 | `"cwmpWeb" "main.acs.telefonica.net"` | [proven](ACS-HUNT.md) |
| <a id="ruijie-cpe"></a>RUIJIE-CPE | cpe | 474 | 2026-11-01T09:17:27+00:00 | `"RUIJIE-CPE"` | [proven](NOTES.md) |
| <a id="easycwmp-fork-ltecpe"></a>easycwmp fork: ltecpe | cpe | 91 | 2026-11-01T09:17:26+00:00 | `"realm@ltecpe"` | [proven](NOTES.md) |
| <a id="openacs"></a>openacs | acs | 17 | 2026-11-01T09:17:31+00:00 | `"openacs"` | [proven](NOTES.md) |
| <a id="axiros"></a>Axiros | acs | 6 | 2026-11-01T09:17:32+00:00 | `"Axiros"` | [proven](NOTES.md) |
| <a id="freeacs"></a>FreeACS Web | acs | 6 | 2026-11-01T09:17:33+00:00 | `http.title:"FreeACS"` | [title signature; public reports](PUBLIC-DISCLOSURES.md#freeacs-20261012) |
| <a id="rompager"></a>RomPager (all ports) | mixed | 447,478 | 2026-11-01T09:18:01+00:00 | `"RomPager"` | [HTTP component; cloud-cohort screening](LEGACY-HTTP.md#rompager) |
| <a id="mini-httpd"></a>mini_httpd (all ports) | mixed | 196,763 | 2026-11-01T09:18:02+00:00 | `"mini_httpd"` | [HTTP component; cloud-cohort screening](LEGACY-HTTP.md#mini-httpd) |

## Scope and historical corrections

Huawei auxiliary ports are authentication-service slices, not automatically web interfaces. TR069 Client is Works Systems OneAgent TR; DigAuth and fake-Apache trace to the earlier Works Systems openagent branch. Device OEM attribution remains separate. Gateway/TIM vendor attribution remains open. NettyServer/WindTre remains a platform hypothesis. The shared DT/ACSSimTool RFC-example constant is not proof of a shared SDK. AVSystem libcwmp is CPE software; Telefónica cwmpWeb is an ACS frontend.

The original October 8 development sample classified 70% of 300 HTTP-bearing records. This is neither fleet-wide precision nor a current coverage measurement. The default selection includes all lines. Its sum can count the same host in multiple overlapping queries.

Editorial attribution review: 15 October 2026. IgdAuthentication maps to Broadcom CMS tr69c through a public binary anchor. DSLForum CPE Management keeps ID `dt-speedport-sdk`; no measurements were relabeled with a new collection date. The [FOFA comparison](CROSS-INDEX.md) is separate from this Shodan registry.

RomPager and mini_httpd cover all ports and are labeled as general HTTP components within the all-line selection. Their [cloud-network slices](LEGACY-HTTP.md#honeypots) preserve suspected sensor contamination separately from the raw totals.
