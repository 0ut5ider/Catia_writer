#!/bin/bash
# PullPush sweep for CATIA format topics
OUT=reddit-pullpush.jsonl
UA="research-agent/1.0"
q1=("catpart format" "catpart reverse" "CATPart hex" "catia file format" "catpart ole" "catpart compound" "3dxml writer" "3dxml convert catpart" "cgr catia lightweight" "cgr format")
for q in "${q1[@]}"; do
  for kind in submission comment; do
    enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")
    url="https://api.pullpush.io/reddit/search/$kind/?q=$enc&size=25"
    curl -s -A "$UA" --max-time 30 "$url" | jq -c --arg q "$q" --arg k "$kind" '.data[]? | {id, kind:$k, subreddit, author, created_utc, year:(.created_utc|floor/31557600+2011|floor), score, title, text:(.selftext // .body // ""), permalink, q, source:"pullpush"}' >> $OUT 2>/dev/null
    sleep 6
  done
done
echo DONE > pp.done
