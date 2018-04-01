#!/bin/bash

MONGODB_HOST="${1:-localhost}"
MONGODB_USER="${2:-admin}"
MONGODB_PASSWORD="${3:-admin}"
INTERVAL="${4:-0}"

HOSTNAME="${COLLECTD_HOSTNAME:-$(hostname)}"

while sleep "$INTERVAL" ; do
    timestamp="$(date +%s)"
    mongostat -h "${MONGODB_HOST}" -u "${MONGODB_USER}" -p "${MONGODB_PASSWORD}" --authenticationDatabase admin --quiet --noheaders -n 1 \
    | while IFS=' ' read insert query update delete getmore command dirty used flushes vsize res qr_qw ar_aw netIn netOut conn time; do
	[ "$insert" = "*0" ] && insert=0
	[ "$query" = "*0" ] && query=0
	[ "$update" = "*0" ] && update=0
	[ "$delete" = "*0" ] && delete=0
        echo "PUTVAL ${HOSTNAME}/mongo/mongostat interval=${INTERVAL} ${timestamp}:${insert:-0}:${query:-0}:${update:-0}:${delete:-0}"
    done
done
