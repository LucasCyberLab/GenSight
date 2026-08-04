#!/usr/bin/env bash
# 将元晟传媒工作台同步到 ClodHost 服务器
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-root@78.47.174.254}"
REMOTE_DIR="${REMOTE_DIR:-/srv/gensight/current}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_clodhost}"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

RSYNC_SSH="ssh -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new"

echo "同步 ${LOCAL_DIR} → ${REMOTE_HOST}:${REMOTE_DIR}"

rsync -avz --delete \
  --exclude '.claude/' \
  --exclude 'data.json' \
  --exclude 'deploy/sync-to-server.sh' \
  -e "${RSYNC_SSH}" \
  "${LOCAL_DIR}/" "${REMOTE_HOST}:${REMOTE_DIR}/"

echo "同步完成。在服务器上执行："
echo "  sudo systemctl restart gensight"
echo "  curl -s http://127.0.0.1:8025/api/data | head -c 80"
