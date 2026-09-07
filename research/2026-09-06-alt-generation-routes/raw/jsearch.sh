#!/bin/bash
# jina+ddg-lite search; usage: jsearch.sh "query" name
Q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")
curl -s --max-time 60 "https://r.jina.ai/https://lite.duckduckgo.com/lite/?q=$Q" -o "searches/$2.md" -w "%{http_code} $2\n"
sleep 2
