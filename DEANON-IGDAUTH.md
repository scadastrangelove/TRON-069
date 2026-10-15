# IgdAuthentication: Broadcom CMS tr69c

Public fingerprint review, 15 October 2026.

The `IgdAuthentication` response family is attributed to the Broadcom CMS
`tr69c` client. A public ZyXEL VMG1312-B10A build tree supplies a reproducible
binary anchor: the realm, challenge parameter order and distinctive fixed
opaque marker occur together in the client. This identifies a software
component lineage. Other manufacturers can ship the same component.

<a id="public-evidence"></a>
## Public evidence

The [VMG1312-B10A build tree](https://github.com/Olipro/VMG1312-B10A/tree/9ae84bc248340f0cb3fb349afffd95a9939a0f02)
identifies its firmware version as `1.00(AAJZ.14)C0`. The inspected file is
[`userspace/private/apps/tr69c/tr69c_VMG1312-B10A_save`](https://github.com/Olipro/VMG1312-B10A/blob/9ae84bc248340f0cb3fb349afffd95a9939a0f02/userspace/private/apps/tr69c/tr69c_VMG1312-B10A_save).

| Property | Value |
| --- | --- |
| Repository commit | `9ae84bc248340f0cb3fb349afffd95a9939a0f02` |
| File size | 682,572 bytes |
| SHA-256 | `dc327b502d6077638c1c2d46a71a17ba35101104f1068fe79c513e6375f02602` |
| Fixed opaque marker, file offset `0x4018c` | `5ccc09c403ebaf9f0171e9517f40e41` |
| Challenge format string, file offset `0x401ac` | See below |
| Realm string, file offset `0x40550` | `IgdAuthentication` |

The challenge format string has this parameter order (a trailing space precedes
the line ending in the binary):

```http
WWW-Authenticate: Digest realm="%s", domain="%s", nonce="%s", qop="auth", algorithm=MD5, opaque="%s"
```

The shortened RFC-example-like opaque value is a useful discriminator when
combined with the realm and response template. No claim of global uniqueness
is made for a literal that can be copied or configured. The binary is linked
at its public source; no firmware is redistributed by this repository.

The binary also references `cmsLog_init` and the CMS libraries
`libcms_msg.so`, `libcms_util.so`, `libcms_boardctl.so` and `libcms_core.so`,
consistent with its placement in the Broadcom CMS client tree.

## Atlas interpretation

The [13 October Shodan record](data/mapdata/snapshot-20261013-160503/igdauthentication.json)
contains 1,540,730 matches for `"IgdAuthentication"`. Its count and collection
time remain unchanged by this attribution update. Port 30005 and 49501 slices
remain overlapping research queries; neither identifies a hardware model.

The DSLForum CPE Management response has a different challenge template.
Its [separate fingerprint note](FINGERPRINTS.md#dslforum-cpe-management) retains
an unresolved supplier. A shared RFC example alone is insufficient evidence
of a common SDK. This dossier records fingerprint evidence only.
