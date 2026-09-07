#!/usr/bin/env python3
"""Emulate the PRONOM internal signatures for CATIA V5 against local samples.

PRONOM x-fmt/439 (catpart) and x-fmt/440 (catproduct) both declare, at absolute
offset 0:

    56355F434656320000*2E43415450617274     (catpart)
    56355F434656320000*2E43415450726F64756374 (catproduct)

That is magic `V5_CFV2` + two 0x00 bytes, then a `*` gap, then the literal
`.CATPart` / `.CATProduct`. In PRONOM syntax `*` is a variable-length gap, so the
signature needs the literal dotted extension somewhere after byte 9.

Run from the repo root:
    python3 research/2026-09-07-container-invariant-sweep/pronom_signature_check.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXED = {
    "x-fmt/439": (bytes.fromhex("56355F434656320000"), b".CATPart"),
    "x-fmt/440": (bytes.fromhex("56355F434656320000"), b".CATProduct"),
}


def main():
    samples = [
        p
        for p in sorted(ROOT.rglob("*"))
        if p.is_file() and p.suffix.lower() in (".catpart", ".catproduct") and p.read_bytes()[:7] == b"V5_CFV2"
    ]
    print(f"{len(samples)} V5_CFV2 samples\n")
    print(f"{'file':32} {'PUID':11} {'fixed b0-8':11} {'literal hit':12} {'PRONOM match':13} class-token hits")
    ok = 0
    for p in samples:
        d = p.read_bytes()
        puid = "x-fmt/439" if p.suffix.lower() == ".catpart" else "x-fmt/440"
        fixed, lit = FIXED[puid]
        fixed_ok = d[: len(fixed)] == fixed
        lit_at = d.find(lit)
        match = fixed_ok and lit_at >= len(fixed)
        ok += match
        token = lit.lstrip(b".").lower()
        toks = sum(1 for t in (b"CATPart", b"CATProduct") if t.lower() in d.lower())
        print(f"{p.name[:32]:32} {puid:11} {str(fixed_ok):11} {str(lit_at):12} {str(match):13} {toks}")
    print(f"\nPRONOM internal signature matches {ok}/{len(samples)} real files.")
    print("Compare: directory_offset + directory_length == file_size holds 10/10 on the same set.")


if __name__ == "__main__":
    main()
