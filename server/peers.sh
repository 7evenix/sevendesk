#!/bin/sh
# Devices registered on the SevenDesk server (hbbs database), newest first:
# ID, first registration (UTC) and the IP it registered from. Unknown IDs or a
# sudden jump in the count mean someone else is using the server: block their
# IPs with firewalld, or rotate the key (README, "Server").
# Usage: server/peers.sh [days]   (default: all)
set -eu
days=${1:-}
where=""
[ -n "$days" ] && where="where created_at >= datetime('now', '-$(printf '%d' "$days") days')"
docker run --rm -v sevendesk-server_sevendesk-data:/data:ro alpine:3.22 sh -c "
apk add -q sqlite >/dev/null
sqlite3 -readonly -header -column /data/db_v2.sqlite3 \"
  select id, created_at, replace(json_extract(info, '\\\$.ip'), '::ffff:', '') as ip
  from peer $where order by created_at desc;\"
echo
sqlite3 -readonly /data/db_v2.sqlite3 \"select count(*) || ' registered devices in total' from peer;\"
"
