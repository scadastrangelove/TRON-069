# ACS and CPE research sweep

Public edition of the 10 October 2026 investigation. Historical sample counts
below describe that research pass. The current atlas uses separately dated Count
results. A visible service or software version is not proof of vulnerability.

## cwmp-server

The lowercase `Server: cwmp server` response, uppercase date and 404 status formed
a distinct previously unregistered signature. The historical count was 84,418,
with concentrations in Brazil, Ukraine, South Africa, Taiwan and Belarus. Ports
included 7547, 7548 and 8069. Its manufacturer and CPE/ACS role remain unknown.
A 404 on GET does not establish that the service expects POST.

The response pattern was consistent across 100 inspected banners. Twelve host
records did not reveal a companion web interface. A separate 25-record check
found no Ruijie markers. These are bounded negatives. Checked RDK log strings and
honeypot configurations did not establish an attribution.

Operator facets include Lanet, Hsin Yeong An Cable, VIPTURBO, Cool Ideas and A1.
An operator equipment catalog suggests candidates, including TOTOLINK, but a
catalog listing does not prove which implementation produces this response.

## telefonica-cwmpweb

The `/cwmpWeb` path and `main.acs.telefonica.net` cookie domain support attribution
to a Telefónica ACS frontend. The historical query returned 1,483 matches, mostly
in Spain, with gSOAP/2.7 and BIG-IP response markers. This is an ACS line and is
excluded from the default CPE-oriented signature sum. No exploitability conclusion
or active test follows from the advertised toolkit version.

## acssimtool

The original component vendor remains unresolved. A public Python reimplementation
uses the same realm; it does not establish the original vendor, deployed code or
deployed credentials. Repeated response values in a small sample do not prove
fleet-wide invariance or successful replay. The exact sample-marker query is retained in the collection catalog. New
vulnerability findings and reproduction details are outside this release.

## nettyserver

The historical 30,415-match slice was concentrated in Italy on port 7547, with
Basic authentication and lowercase headers. WindTre association remains an
operator/platform hypothesis rather than a demonstrated manufacturer attribution.

## avsystem-libcwmp

AVSystem libcwmp is a CPE component, not an ACS server. A 100-banner sample was
mostly version 5.7.9, followed by 5.6.2 and a small 5.5.3 tail. Those percentages
are not the population distribution. The collector now counts the known version
queries and a same-run total separately; unmatched versions remain a remainder.

## obuspa

The inspected WebSocket server uses libwebsockets without a distinct application
HTTP banner. No separate atlas line was added. Lack of a useful HTTP signature
does not imply that no agents are deployed; MQTT/STOMP transport further limits
what HTTP banner searches can establish.

## Singtel, Netis and RAC2V1K

Singtel cross-service observations, three Netis retail negatives and four
RAC2V1K repository checks are summarized in
[DEANON-TR069CLIENT.md](DEANON-TR069CLIENT.md). Co-hosting does not prove one
firmware image, and a finite search does not prove global absence.

Update, 13 October: public Nokia and ASUS binaries, ASUS build metadata and
Works Systems copyrights identify the main TR069 Client component as
**Works Systems OneAgent TR**. The RAC2V1K/F609/Arcadyan acquisition hunts are
closed for component attribution. The dossier records the evidence and the
remaining EZpacket distribution hypothesis.

## gateway-realm

The scoped query on port 7170 is strongly associated with Telecom Italia/TIM.
The research log's organization facets and 200-banner ISP sample supported this
association. It must not be generalized to every service using realm Gateway.

Technicolor and ADB remain candidates. A later writeup claimed a closed
Technicolor attribution after inspecting a TIM TG789vac image, but that image
used port 51007 and did not contain the observed Gateway realm. A similar Digest
template does not resolve those gaps. The claimed integer-overflow explanation
also confused printf field width with value length. The public atlas therefore
keeps attribution open and records the 51007 control query separately.

## Atlas integration

The two new lines are `cwmp-server` and `telefonica-cwmpweb`. Other results appear
as qualified findings, separate research variants and project-news entries.
See [data/research-findings.json](data/research-findings.json) for coverage.
Firmware extracts, host addresses and unpublished security details are excluded.
