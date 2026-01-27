#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class FileEntry:
    name: str
    size: int
    sha256: str


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _env_root_from_here() -> Path:
    here = Path(__file__).resolve()
    env_root = here.parents[1]  # .../environment/scripts -> .../environment
    if env_root.name != "environment":
        raise RuntimeError(f"Unexpected script location: {here}")
    return env_root


def _sweph_dir() -> Path:
    return _env_root_from_here() / "data" / "sweph"


def build() -> None:
    sweph_dir = _sweph_dir()
    if not sweph_dir.exists():
        raise SystemExit(f"Missing directory: {sweph_dir}")

    entries: list[FileEntry] = []
    for p in sorted(sweph_dir.iterdir(), key=lambda x: x.name):
        if not p.is_file():
            continue
        if p.name in ("manifest.json", "SHA256SUMS.txt", "README.md", ".DS_Store"):
            continue
        entries.append(FileEntry(name=p.name, size=p.stat().st_size, sha256=_sha256(p)))

    created_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "created_at_utc": created_at,
        "source": {
            "name": "Swiss Ephemeris (Alois Treindl)",
            "repo": "https://github.com/aloistr/swisseph",
            "path": "ephe/",
            "note": "Downloaded during setup. Do not update silently; re-run build+verify if changed.",
        },
        "files": [e.__dict__ for e in entries],
    }

    (sweph_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [f"{e.sha256}  {e.name}" for e in entries]
    (sweph_dir / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {sweph_dir / 'manifest.json'}")
    print(f"Wrote {sweph_dir / 'SHA256SUMS.txt'}")


def verify() -> None:
    sweph_dir = _sweph_dir()
    manifest_path = sweph_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest: {manifest_path} (run build first)")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {f["name"]: f["sha256"] for f in manifest.get("files", [])}

    mismatches: list[str] = []
    missing: list[str] = []
    extra: list[str] = []

    present = {p.name for p in sweph_dir.iterdir() if p.is_file()}
    for name in sorted(expected.keys()):
        p = sweph_dir / name
        if not p.exists():
            missing.append(name)
            continue
        got = _sha256(p)
        if got != expected[name]:
            mismatches.append(f"{name}: expected {expected[name]} got {got}")

    for name in sorted(present - set(expected.keys())):
        if name in ("manifest.json", "SHA256SUMS.txt", "README.md", ".DS_Store"):
            continue
        extra.append(name)

    if missing or mismatches or extra:
        if missing:
            print("Missing files:")
            for m in missing:
                print(f"- {m}")
        if mismatches:
            print("Mismatched files:")
            for m in mismatches:
                print(f"- {m}")
        if extra:
            print("Extra files (not in manifest):")
            for m in extra:
                print(f"- {m}")
        raise SystemExit(1)

    print("OK: all Swiss Ephemeris files match manifest.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="sweph_manifest.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("verify")
    args = parser.parse_args()

    if args.cmd == "build":
        build()
    elif args.cmd == "verify":
        verify()
    else:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
