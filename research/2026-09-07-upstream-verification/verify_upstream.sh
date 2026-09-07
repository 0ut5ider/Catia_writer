#!/usr/bin/env bash
# Re-run the 2026-09-07 upstream verification checks. Needs network.
# Writes into research/2026-09-07-upstream-verification/raw/.
set -uo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
OUT="$HERE/raw"
mkdir -p "$OUT"

echo "== 1. cadmpeg exists and is decode-only for CATIA =="
curl -s https://api.github.com/repos/cadmpeg/cadmpeg \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["full_name"],d["created_at"],d["pushed_at"],d["stargazers_count"],(d.get("license") or {}).get("spdx_id"))' \
  > "$OUT/cadmpeg-repo.json.txt"
curl -s https://raw.githubusercontent.com/cadmpeg/cadmpeg/main/docs/api-baseline/cadmpeg-codec-catia.txt \
  > "$OUT/cadmpeg-api-baseline-catia.txt"
curl -s https://raw.githubusercontent.com/cadmpeg/cadmpeg/main/docs/api-baseline/cadmpeg-codec-step.txt \
  > "$OUT/cadmpeg-api-baseline-step.txt"
grep -c encode "$OUT/cadmpeg-api-baseline-catia.txt" || echo "0 encode symbols in the CATIA codec API baseline"

echo "== 2. open-source OCCT has no CATIA code =="
# The full tree JSON is 11 MB and regenerable, so only the derived summary is kept.
curl -s "https://api.github.com/repos/Open-Cascade-SAS/OCCT/git/trees/master?recursive=1" -o /tmp/occt-tree.json
python3 - /tmp/occt-tree.json <<'PY' > "$OUT/occt-master-no-catia.txt"
import json,sys,datetime
t=json.load(open('/tmp/occt-tree.json'))['tree']
hits=[x['path'] for x in t if 'catia' in x['path'].lower()]
print(f"checked {datetime.date.today()} against Open-Cascade-SAS/OCCT master")
print(f"tree entries: {len(t)}")
print(f"paths containing 'catia': {len(hits)}")
for h in hits: print('  ', h)
PY
rm -f /tmp/occt-tree.json
cat "$OUT/occt-master-no-catia.txt"

echo "== 3. PRONOM identity check (fmt/1615 is CATIA Drawing, not settings) =="
curl -s https://raw.githubusercontent.com/nationalarchives/pronom/develop/signatures/fmt/1615.json \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);r=d[0] if isinstance(d,list) else d;print(r.get("formatName"),r.get("version"))' \
  > "$OUT/pronom-fmt-1615.txt"

echo "== 4. V5_CFV4 constant source (KaiUR/Pycatia_Scripts) =="
curl -s https://raw.githubusercontent.com/KaiUR/Pycatia_Scripts/main/Utility_Scripts/Show_CATIA_File_Info.py \
  | grep -n "V5_MAGIC\|V5R(" > "$OUT/kaiur-magic-constants.txt"

echo done
