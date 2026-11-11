# Research specimens

Inspected firmware, source trees, bounded negative results and reported leads.
Related atlas lines identify the research question. Partial, negative and pending
records do not assign a device to a measured fleet.

Reviewed: **2026-11-11**. 15 records.

[Browse in the atlas](https://scadastrangelove.github.io/TRON-069/#lang=en&tab=wanted)

<!-- Generated from data/research-specimens.json by tools/build-map.py. -->

| Sample | Material | Result | Verification |
| --- | --- | --- | --- |
| [TP-Link Archer VR1600v V2](#tplink-vr1600v-v2) | Firmware image | Match in sample | Artifact checked |
| [ZTE ZXHN H108N](#zte-h108n) | Firmware image | Match in sample | Published research note |
| [ZTE F670L · V1.1 / V9.0](#zte-f670l) | Firmware image | Match in sample | Published research note |
| [Huawei HG8145V5](#huawei-hg8145v5) | Firmware image | Match in sample | Published research note |
| [Huawei EG8145V5](#huawei-eg8145v5) | Firmware image | Awaiting verification | Reported lead |
| [D-Link DIR-615 · AthSDK GPL](#dir615-openagent) | Source code | Match in sample | Artifact checked |
| [ASUS asuswrt · OneAgent TR](#asus-oneagent) | Source code | Match in sample | Artifact checked |
| [Technicolor TG789vac · TIM](#technicolor-tg789vac) | Binary / dump | Scoped negative | Published research note |
| [ZyXEL VMG1312-B10A](#zyxel-vmg1312) | Binary / dump | Match in sample | Artifact checked |
| [ZyXEL C1000Z · CenturyLink](#zyxel-c1000z) | Binary / dump | Match in sample | Published research note |
| [ZyXEL C1100Z · CenturyLink](#zyxel-c1100z) | Binary / dump | Match in sample | Published research note |
| [Sky SR102](#sky-sr102) | Binary / dump | Awaiting verification | Reported lead |
| [Nokia FastMile 5G Gateway 3.2](#nokia-fastmile-32) | Binary / dump | Match in sample | Artifact checked |
| [Arcadyan ARV7519RW22 · Orange](#arcadyan-arv7519rw22) | Firmware container | Partial extraction | Reported lead |
| [Speedport W723V](#speedport-w723v) | Firmware image | Scoped negative | Reported lead |

<a id="tplink-vr1600v-v2"></a>
## TP-Link Archer VR1600v V2

The extracted cwmp contains tr069 http server and the response-header markers of the Works Systems openagent lineage. The official archive was downloaded again and the extracted binary hash matched.

Result: **Match in sample**. Evidence: Artifact checked.

Related research: `tr069-http-server`.

Version: `0.1.0 Build 260317 Rel.7757n`.

- [Archer VR1600v V2 · /usr/bin/cwmp (inside official firmware archive)](https://static.tp-link.com/upload/firmware/2026/202604/20260408/Archer_VR1600vV2_0.1.0_0.9.1_up_boot%28260317%29_2026-03-17_10.25.18.bin.zip) — SHA-256 `2aa70f71350cdc59606e3d10ef7b0ce25b85d1eedd3a4058f42ef6b45774fc28`.

Research: [FINGERPRINTS.md](FINGERPRINTS.md#tplink-works-lineage).

<a id="zte-h108n"></a>
## ZTE ZXHN H108N

The inspected httpd and cspd anchor CPE-SERVER/1.0 and cpe@zte.com. Local extracted-file hashes are recorded; the exact source archive and version still need a public citation.

Result: **Match in sample**. Evidence: Published research note.

Related research: `cpe-server-1-0`, `zte`, `mini-web-server-1-0-zte-corp`.

- Extracted `bin/httpd` — SHA-256 `ed2d28b7557ce5f4ced8d4ba46574e188953d383a075dd9e373da915160bfb91`.

- Extracted `cspd` — SHA-256 `951876f5be0b174f59e3e4d223f42ec94ca0d7036eb4ed4d11cc64c4f8eaddd1`.

Still needed: public artifact source, exact release / revision.

Research: [NOTES.md](NOTES.md#section-9.17).

<a id="zte-f670l"></a>
## ZTE F670L · V1.1 / V9.0

Two inspected generations contain cpe@zte.com and default CR port 58000. The separate search for the TR069 Client brand was negative in these artifacts. Both results can hold for the same firmware.

Result: **Match in sample**. Evidence: Published research note.

Related research: `zte`, `cpe-server-1-0`.

Version: `V1.1.20P3N4D / V9.0.11P1N36`.

Still needed: public artifact source, binary hash.

Research: [NOTES.md](NOTES.md#section-9.31) · [NOTES.md](NOTES.md#section-9.34) · [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md).

<a id="huawei-hg8145v5"></a>
## Huawei HG8145V5

The inspected image configures a CR listener on port 30005. This is a platform reference; the Huawei response does not identify every matching device model.

Result: **Match in sample**. Evidence: Published research note.

Related research: `huaweihomegateway`, `huaweihomegateway-cr-slice`.

Still needed: public artifact source, exact release / revision, binary hash.

Research: [DEANON-HUAWEI-CR.md](DEANON-HUAWEI-CR.md) · [NOTES.md](NOTES.md#section-9.31).

<a id="huawei-eg8145v5"></a>
## Huawei EG8145V5

Reported alongside HG8145V5. A separate EG8145V5 artifact has not been independently tied to the public fingerprint evidence.

Result: **Awaiting verification**. Evidence: Reported lead.

Related research: `huaweihomegateway`.

Still needed: public artifact source, exact release / revision, binary hash, CR-template comparison.

Research: [FINGERPRINTS.md](FINGERPRINTS.md#specimen-review-20261111).

<a id="dir615-openagent"></a>
## D-Link DIR-615 · AthSDK GPL

The GPL file carries the Works Systems 2006–2007 copyright and the connection-request response template. It anchors the earlier openagent branch.

Result: **Match in sample**. Evidence: Artifact checked.

Related research: `digauth`, `fake-apache-openagent`, `tr069-http-server`.

Version: `openagent-2.0`.

- [DIR-615 AthSDK · conn_req_server.c](https://github.com/nist/DIR-615/blob/272e8bbe56907d3d89e8409f4de1552b63055823/GPL_Source_Code/src/AthSDK/apps/openagent-2.0/src/tools/conn_req_server.c#L2) — SHA-256 `7fff1cfcb61b21424aedf9eec8bcedf02cc701532c1a2ffa447cf8e2e8cb0f7c`.

Research: [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md#public-evidence).

<a id="asus-oneagent"></a>
## ASUS asuswrt · OneAgent TR

Copyright and build metadata name Works Systems OneAgent TR. A public prebuilt client supplies a corresponding 401 template; each artifact is pinned separately.

Result: **Match in sample**. Evidence: Artifact checked.

Related research: `tr069-client`.

- [ASUS asuswrt · tr.h](https://github.com/smx-smx/asuswrt-rt/blob/81404a37312b7707c29de12c3a38ef7e50eea3c8/apps/private/tr069/include/tr.h#L3) — SHA-256 `16cdbca47c18f6284b7922ff116dc27fbd9d70fee5505a7d82d7cb7d6a0479e4`.

- [ASUS asuswrt · Makefile.DSL_ASUSWRT](https://github.com/smx-smx/asuswrt-rt/blob/81404a37312b7707c29de12c3a38ef7e50eea3c8/apps/private/tr069/Makefile.DSL_ASUSWRT#L82) — SHA-256 `716c82e8b384c84defb2fd34de908cf00b41dd372fba6378139ef029e0c9dde6`.

- [ASUS asuswrt-merlin · prebuild/tr](https://github.com/gnuton/asuswrt-merlin.ng/blob/14166d1af5fc9a115c66f187e1618977b732682d/release/src/router/tr069/prebuild/tr) — SHA-256 `6ccb9cf73731b4eb70a264b845bce477512f468fbda329b98f58815b61b55d94`.

Research: [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md#public-evidence).

<a id="technicolor-tg789vac"></a>
## Technicolor TG789vac · TIM

The inspected image used port 51007 and lacked the observed Gateway realm. It does not close attribution of the Gateway:7170 population. This is a binary review, not source-code proof.

Result: **Scoped negative**. Evidence: Published research note.

Related research: `gateway-realm`.

Still needed: public artifact source, exact release / revision, binary hash.

Research: [ACS-HUNT.md](ACS-HUNT.md) · [ACS-URL-MINING.md](ACS-URL-MINING.md).

<a id="zyxel-vmg1312"></a>
## ZyXEL VMG1312-B10A

The public tr69c binary matches IgdAuthentication, the challenge parameter order and the fixed opaque marker. CMS symbols and library references identify the Broadcom component.

Result: **Match in sample**. Evidence: Artifact checked.

Related research: `igdauthentication`.

Version: `1.00(AAJZ.14)C0`.

- [ZyXEL VMG1312-B10A · tr69c](https://github.com/Olipro/VMG1312-B10A/blob/9ae84bc248340f0cb3fb349afffd95a9939a0f02/userspace/private/apps/tr69c/tr69c_VMG1312-B10A_save) — SHA-256 `dc327b502d6077638c1c2d46a71a17ba35101104f1068fe79c513e6375f02602`.

Research: [DEANON-IGDAUTH.md](DEANON-IGDAUTH.md#public-evidence).

<a id="zyxel-c1000z"></a>
## ZyXEL C1000Z · CenturyLink

The reviewed tree contains Broadcom CMS tr69c alongside WPS Monitor. The reported identical CR-template comparison still needs exact binary hashes and public revisions.

Result: **Match in sample**. Evidence: Published research note.

Related research: `igdauthentication`.

Still needed: public artifact source, exact release / revision, binary hash, CR-template comparison.

Research: [NOTES.md](NOTES.md#section-9.44) · [FINGERPRINTS.md](FINGERPRINTS.md#specimen-review-20261111).

<a id="zyxel-c1100z"></a>
## ZyXEL C1100Z · CenturyLink

The reviewed tree contains Broadcom CMS tr69c alongside WPS Monitor. The reported identical CR-template comparison still needs exact binary hashes and public revisions.

Result: **Match in sample**. Evidence: Published research note.

Related research: `igdauthentication`.

Still needed: public artifact source, exact release / revision, binary hash, CR-template comparison.

Research: [NOTES.md](NOTES.md#section-9.44) · [FINGERPRINTS.md](FINGERPRINTS.md#specimen-review-20261111).

<a id="sky-sr102"></a>
## Sky SR102

Reported as an additional carrier in the tr69c cross-comparison. The matching binary, revision and response template have not yet been supplied in the public evidence bundle.

Result: **Awaiting verification**. Evidence: Reported lead.

Related research: `igdauthentication`.

Still needed: public artifact source, exact release / revision, binary hash, CR-template comparison.

Research: [FINGERPRINTS.md](FINGERPRINTS.md#specimen-review-20261111).

<a id="nokia-fastmile-32"></a>
## Nokia FastMile 5G Gateway 3.2

The public tr_agent matches the complete OneAgent 401 template and contains Workssys identification strings. The dump revision and file hash are pinned.

Result: **Match in sample**. Evidence: Artifact checked.

Related research: `tr069-client`.

- [Nokia FastMile 5G Gateway 3.2 · tr_agent](https://github.com/natumbri/FastMile_5G_Gateway_3.2/blob/3bb8cce2dcf74e97a292574bbfc69a811bb5e7ea/firmware/usr/bin/tr_agent) — SHA-256 `c964db3a877d8a0d58ac7531b8b1caab2faaeba81de4d9192ad6be24651880ed`.

Research: [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md#public-evidence).

<a id="arcadyan-arv7519rw22"></a>
## Arcadyan ARV7519RW22 · Orange

The research report describes a parsed BRN container with the root filesystem still inaccessible. No CR signature match follows from the container structure.

Result: **Partial extraction**. Evidence: Reported lead.

Related research: `tr069-client`.

Still needed: public artifact source, exact release / revision, binary hash, CR-template comparison.

Research: [FINGERPRINTS.md](FINGERPRINTS.md#specimen-review-20261111) · [DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md).

<a id="speedport-w723v"></a>
## Speedport W723V

The research report says the sought fingerprint was absent in one inspected firmware. The hardware variant and exact release are not recorded here; this result cannot be extended to every W723V build.

Result: **Scoped negative**. Evidence: Reported lead.

Related research: `dt-speedport-sdk`.

Still needed: public artifact source, hardware variant, exact release / revision, binary hash.

Research: [FINGERPRINTS.md](FINGERPRINTS.md#specimen-review-20261111).
