# Container invariant sweep over the local CATIA V5 corpus

- Date: 2026-09-07
- Role: verification pass, run against files already in this repository
- Question asked: do the container invariants that cadmpeg documents in
  `docs/formats/catia.md` section 3.1 hold across every native sample we have, and is
  the PRONOM signature recommendation in `FINDINGS.md` safe to build detection on
- Model: flashnext/flashnext-w4a16-fp8ple

Reproduce with `python3 container_sweep.py` and `python3 pronom_signature_check.py`
from the repo root. Full output is in `container-sweep-output.txt` and
`pronom-signature-check-output.txt`.

## Corpus

10 native files from four different swarm efforts and four sources, V5R14 through V5R30:

| file | size | dir_off | dir_len | off+len==size | ff*8 @0x10 | 00*32 @0x18 | hdr_flags @0x38 | CB__END | inner V5_CFV2 | FINJPL | release tag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sample2.CATPart | 76,575 | 66,397 | 10,178 | yes | yes | yes | `000000025f0d0a00` | 2 | 1 | 12 | V5R20SP0HF0 |
| sample_assembly.CATProduct | 90,859 | 84,049 | 6,810 | yes | yes | yes | `000000025f0d0a00` | 1 | 0 | 7 | V5R20SP0HF0 |
| analysis.catpart | 15,186 | 11,948 | 3,238 | yes | yes | yes | `000000025f0d0a00` | 1 | 0 | 4 | V5R24SP4HF0 |
| brepaccess.catpart | 11,436 | 8,202 | 3,234 | yes | yes | yes | `000000025f0d0a00` | 1 | 0 | 4 | V5R27SP0HF0 |
| catconduit.catpart | 15,106 | 11,860 | 3,246 | yes | yes | yes | `000000025f0d0a00` | 1 | 0 | 4 | V5R25SP4HF0 |
| motor.CATProduct | 381,724 | 372,884 | 8,840 | yes | yes | yes | `000000025f0d0a00` | 1 | 0 | 9 | V5R21SP0HF0 |
| spur_gear.CATPart | 481,357 | 471,773 | 9,584 | yes | yes | yes | `000000025f0d0a00` | 2 | 1 | 11 | V5R21SP0HF0 |
| MM_Oil_Dipstick.CATPart | 227,597 | 217,117 | 10,480 | yes | yes | yes | `000000025f0d0a00` | 2 | 1 | 12 | V5R30SP6HF0 |
| Part1.CATPart | 112,111 | 100,847 | 11,264 | yes | **no** | yes | `000000005f0d0a00` | 3 | 1 | 12 | none, reads `CATIAV5R14` |
| Print.CATProduct | 14,975 | 9,855 | 5,120 | yes | yes | yes | `000000005f0d0a00` | 1 | 0 | 4 | none |

## What holds

1. `u32be(0x08) + u32be(0x0C) == file_size`, 10/10. cadmpeg's core container invariant
   survives a real corpus across 16 releases. This is the invariant to build on.
2. `00 * 32` at `0x18..0x37`, 10/10.
3. Directory at `dir_off` starts with `CATIA_V5 CB0001\0` and the file carries a
   `CB__END\0` sentinel, 10/10.
4. No file is OLE2/CFB. `D0CF11E0` never appears at offset 0, 0/10. The
   compound-storage theory is dead, permanently.
5. `V5_CFV4` appears 0 times across all 10 files, in any position. See the correction in
   `../2026-09-07-upstream-verification/upstream-verification.md`.

## What is conditional

6. `ff * 8` at `0x10..0x17` fails on `Part1.CATPart`, the V5R14-era file. cadmpeg
   documents that field for the current band and marks release-band coverage open. Treat
   it as descriptive, not as a validator.
7. `hdr_flags` at `0x38..0x3F` takes exactly two values in this corpus:
   `00000002 5f0d0a00` for V5R20 and later, `00000000 5f0d0a00` for the two files with no
   `SP`/`HF` release tag. The trailing `5f 0d 0a 00` (`_`, CR, LF, NUL) is constant.
   Twelve data points, one confound: the two populations differ in release tag too, so
   this does not separate version from document age. Do not use it for release detection.
8. The nested inner `V5_CFV2` appears in 4 files, all of them CATParts with real B-rep.
   Every CATProduct here has 0 inner containers, and the three smallest CATParts
   (`analysis`, `brepaccess`, `catconduit`) have none either. cadmpeg says the inner
   container holds the fragmented BREP streams, so the correlation is expected. It also
   means a template-patch writer for `.catproduct` does not need the inner container at
   all, which is the cheapest part of the whole format.
9. `CB__END` count is 1 in files without an inner container and 2 or 3 in files with one,
   so each container closes itself and a hand-built file must emit the right count.

## The PRONOM recommendation in FINDINGS.md is unsafe

PRONOM `x-fmt/439` declares an internal signature at absolute offset 0:

```
56355F434656320000*2E43415450617274
```

That is `V5_CFV2` plus two zero bytes, then a `*` gap, then the literal `.CATPart`. PRONOM
`*` is a variable-length gap, so the signature requires the dotted extension string to
exist somewhere after byte 9. Tested in `pronom_signature_check.py`:

- **2 of 10 files match** (`Part1.CATPart`, `Print.CATProduct`).
- 8 of 10 contain no `.CATPart` or `.CATProduct` string anywhere, in any case.
- Three of those eight (`analysis.catpart`, `brepaccess.catpart`, `catconduit.catpart`)
  contain no `CATPart` substring at all, even case-insensitively. They come from the
  PRONOM test corpus at `github.com/glepore70/pronom-research`, the very corpus used to
  validate PRONOM signatures.

Why it fails: the token `CATPart`/`CATProduct` in these files is class and schema
vocabulary, not a filename. Typical context is `..._Name _Shapes FromCATPart IsRoot...` in
CATParts and `CATUnicodeString ... CATProduct ...` in CATProducts. Only some documents
store the original filename with its extension, as a summary `CATUnicodeString` value.

Practical rule for detection code:

1. Require `V5_CFV2\0` at offset 0.
2. Require `u32be(8) + u32be(12) == file_size`.
3. Require `CATIA_V5 CB0001\0` at the directory offset and a `CB__END\0` in that region.
4. Use the PRONOM PUID only as a label attached to the above, never as the test itself.
5. Do not branch on file extension, and do not treat the absence of an in-file filename
   string as a rejection.

`FINDINGS.md` said PRONOM signatures are "useful for safe detection". Corrected there: they
are safe to *cite* and unsafe to *depend on*.
