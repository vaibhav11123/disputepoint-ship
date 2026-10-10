#!/usr/bin/env bash
# Stage a minimal Lambda payload: backend + fixtures (no frontend/.venv/node_modules).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PKG="$ROOT/infra/package"
rm -rf "$PKG"
mkdir -p "$PKG"
rsync -a --delete \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.pytest_cache' \
  "$ROOT/backend/" "$PKG/backend/"
mkdir -p "$PKG/data"
rsync -a --delete "$ROOT/data/fixtures/" "$PKG/data/fixtures/"
# Optional audit L1 (no L0 bodies)
if [[ -d "$ROOT/data/audit" ]]; then
  rsync -a --delete \
    --exclude 'sources/' \
    --exclude '_work/' \
    "$ROOT/data/audit/" "$PKG/data/audit/" || true
fi
cp "$ROOT/infra/requirements.txt" "$PKG/requirements.txt"
# Marker so repo_root() (parents[3] from ingest.py) resolves to package root.
touch "$PKG/.disputepoint_root"
echo "Staged Lambda package at $PKG"
du -sh "$PKG" "$PKG/backend" "$PKG/data" 2>/dev/null || true
