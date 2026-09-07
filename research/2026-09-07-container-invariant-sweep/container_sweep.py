#!/usr/bin/env python3
"""Check cadmpeg catia.md section 3.1/3.2/3.3 container invariants across every
native CATIA V5 sample in this repository. Run from the repo root.

Usage: python3 research/2026-09-07-container-invariant-sweep/container_sweep.py
"""

import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAGIC = b"V5_CFV2\0"
VER = re.compile(rb"V5R(\d+)SP(\d+)HF(\d+)")


def u32be(d, off):
    return struct.unpack_from(">I", d, off)[0] if off + 4 <= len(d) else None


def probe(path):
    d = path.read_bytes()
    n = len(d)
    out = {"file": str(path.relative_to(ROOT)), "size": n}
    if d[:8] != MAGIC:
        out["magic"] = "NOT V5_CFV2: " + repr(d[:8])
        return out
    out["magic"] = "V5_CFV2\\0"
    out["byte08"] = d[8]
    out["byte09_0a"] = d[9:11].hex()
    doff, dlen = u32be(d, 8), u32be(d, 12)
    out["dir_off"], out["dir_len"] = doff, dlen
    out["off_plus_len_eq_size"] = (doff is not None and dlen is not None and doff + dlen == n)
    out["fill_ff_at_10"] = d[0x10:0x18] == b"\xff" * 8
    out["fill_00_at_18"] = d[0x18:0x38] == b"\x00" * 32
    out["hdr_flags_38"] = d[0x38:0x40].hex()
    out["dir_magic"] = d[doff : doff + 16].rstrip(b"\0").decode("latin1") if doff and doff < n else None
    out["cb_end"] = d.count(b"CB__END\0")
    out["inner_v5_cfv2"] = d.count(MAGIC, 8)
    out["finjpl"] = d.count(b"FINJPL  ")
    out["cgm"] = d.count(b"CGM")
    out["cls_tags"] = {t: d.count(t.encode()) for t in ("CATProdCont", "CATFeatCont", "CATPrtCont", "CATDrwCont")}
    m = VER.search(d)
    out["release"] = m.group(0).decode() if m else None
    out["ole_cfb"] = d[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
    out["cfv4"] = d.count(b"V5_CFV4")
    if doff and doff < n:
        out["tail_dir_ascii_sample"] = re.sub(rb"[^\x20-\x7e]", b".", d[doff : min(doff + 160, n)]).decode()
    return out


def main():
    samples = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in {".catpart", ".catproduct", ".catdrawing", ".catmaterial", ".catsettings"}:
            continue
        if d := open(p, "rb").read(8)[:8]:
            if d in (MAGIC, b"V5_CFV4\0"):
                samples.append(p)
    rows = [probe(p) for p in samples]
    keys = [k for k in rows[0]] if rows else []
    print(f"{len(rows)} native samples, invariants from cadmpeg catia.md 3.1-3.3\n")
    for r in rows:
        print(f"--- {r['file']} ({r['size']} B)")
        for k in keys:
            if k == "file":
                continue
            print(f"      {k:24} {r[k]}")
    print("\nAGGREGATE")
    for k in ("off_plus_len_eq_size", "fill_ff_at_10", "fill_00_at_18", "ole_cfb", "cfv4"):
        vals = [r.get(k) for r in rows if k in r]
        print(f"      {k:24} {sum(1 for v in vals if v)}/{len(vals)} true")


if __name__ == "__main__":
    main()
