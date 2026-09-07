import re, sys, glob, urllib.parse
for f in sorted(glob.glob("searches/*.md")):
    txt = open(f).read()
    print("#" * 20, f)
    # numbered entries: N.[Title](https://duckduckgo.com/l/?uddg=<enc>&rut=...)
    for m in re.finditer(r'\d+\.\[(.*?)\]\(https://duckduckgo\.com/l/\?uddg=([^&]+)&rut=[^)]*\)\n(.*?)(?=\n\d+\.|\Z)', txt, re.S):
        title, enc, rest = m.group(1), m.group(2), m.group(3)
        url = urllib.parse.unquote(enc)
        snip = " ".join(rest.split())[:220]
        print(f"URL: {url}\n  T: {title}\n  S: {snip}\n")
