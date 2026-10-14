#!/bin/bash
# High-concurrency load test to demonstrate backend traffic and trigger HPA scaling
TARGET_URL=${1:-"http://localhost:8000/api/incidents"}
CONCURRENCY=${2:-10}
REQUESTS=${3:-1000}

echo "==> Starting load generator against: $TARGET_URL"
echo "==> Concurrency: $CONCURRENCY | Requests: $REQUESTS"

seq 1 "$REQUESTS" | xargs -n 1 -P "$CONCURRENCY" -I {} curl -s -o /dev/null -w "%{http_code}\n" "$TARGET_URL" | sort | uniq -c

echo "==> Load generation finished."
