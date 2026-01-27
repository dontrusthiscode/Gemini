#!/usr/bin/env bash
set -euo pipefail

# Bootstrap the Cardano Engine capsule.
# Network is used here (setup-only). Computation is offline.

ENV_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_DIR="$(cd "$ENV_DIR/.." && pwd)"

UV_BIN="$ENV_DIR/bin/uv"
if [[ ! -x "$UV_BIN" ]]; then
  if command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
  else
    echo "uv not found. Install uv or place it at $ENV_DIR/bin/uv" >&2
    exit 1
  fi
fi

PY_DIR="$ENV_DIR/python"
export UV_PYTHON_INSTALL_DIR="$PY_DIR"

echo "[1/3] Ensure Python 3.12.12 in $PY_DIR"
if [[ ! -d "$PY_DIR" ]] || [[ -z "$("$UV_BIN" --no-python-downloads python find 3.12.12 2>/dev/null || true)" ]]; then
  "$UV_BIN" --cache-dir "$ENV_DIR/uv-cache" python install 3.12.12 --install-dir "$PY_DIR" --force
fi

PY_BIN="$("$UV_BIN" --no-python-downloads python find 3.12.12)"

echo "[2/3] Ensure Swiss Ephemeris data in $ENV_DIR/data/sweph"
SWE_DIR="$ENV_DIR/data/sweph"
mkdir -p "$SWE_DIR"

if [[ -f "$SWE_DIR/manifest.json" ]]; then
  "$PY_BIN" "$ENV_DIR/scripts/sweph_manifest.py" verify
else
  # Download required files from the official Swiss Ephemeris GitHub mirror.
  echo "Downloading Swiss Ephemeris files (this may take a minute)..."
  curl -s https://api.github.com/repos/aloistr/swisseph/contents/ephe \
    | "$PY_BIN" -c 'import json,re,sys; rx=re.compile(r"^(sepl_|semo_|seas_).*\\.se1$|^(seasnam|sefstars|seorbel)\\.txt$"); [print(i.get("name","")) for i in json.load(sys.stdin) if rx.match(i.get("name",""))]' \
    | sort \
    | while IFS= read -r f; do
        curl -L -o "$SWE_DIR/$f" "https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/$f"
      done

  "$PY_BIN" "$ENV_DIR/scripts/sweph_manifest.py" build
  "$PY_BIN" "$ENV_DIR/scripts/sweph_manifest.py" verify
fi

echo "[3/3] Sync Python dependencies (locked) for cardano-engine"
pushd "$ENV_DIR/projects/cardano-engine" >/dev/null
UV_CACHE_DIR="$ENV_DIR/uv-cache" \
UV_PYTHON_INSTALL_DIR="$ENV_DIR/python" \
  "$UV_BIN" sync --frozen
popd >/dev/null

echo "Bootstrap complete."
echo "Run: $REPO_DIR/environment/bin/cardano-engine --input $REPO_DIR/environment/projects/cardano-engine/examples/horary_example.json"
