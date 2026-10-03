#!/bin/bash
# usage: radar.sh "topic"
q="$1"
echo "== HN Show HN (points>100)"; curl -s "https://hn.algolia.com/api/v1/search?query=$(printf %s "$q"|sed 's/ /%20/g')&tags=story&hitsPerPage=8" | python3 -c 'import sys,json;[print(h.get("points"),"|",h.get("title")) for h in json.load(sys.stdin)["hits"]]'
echo "== YouTube metadata"; timeout 90 yt-dlp --flat-playlist --dump-json "ytsearch15:$q" 2>/dev/null | python3 -c 'import sys,json
for l in sys.stdin:
    d=json.loads(l);print(d.get("view_count"),"|",d.get("duration"),"s |",d.get("title"))'
