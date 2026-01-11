```python
/release/nano_translator.py
"""
eArc · Nano Translator (Python)
Status: minimal · deterministic · read-only · stdlib-only

Purpose:
- Load a Frame from:
  - JSON (.json)
  - Markdown with YAML frontmatter (.md)
- Render to human-readable text (no interpretation beyond structure)
- No writing, no modification, no network, no side effects on import

License: MIT (recommendation; align with your repo license)
Source (canonical): iinkognit0.de
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple, Optional


# -----------------------------
# Model
# -----------------------------

@dataclass(frozen=True)
class Frame:
    id: str
    status: str
    created_utc: str
    source: str
    content: str
    meta: Dict[str, Any]


# -----------------------------
# YAML frontmatter (minimal parser)
# stdlib-only: supports "key: value" lines, no nesting.
# -----------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

def _parse_frontmatter(md: str) -> Tuple[Dict[str, str], str]:
    m = _FRONTMATTER_RE.match(md)
    if not m:
        return {}, md.strip()

    raw_yaml = m.group(1)
    body = m.group(2).strip()

    meta: Dict[str, str] = {}
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


# -----------------------------
# Loaders
# -----------------------------

def load_frame(path: Path) -> Frame:
    if not path.exists():
        raise FileNotFoundError(str(path))

    text = path.read_text(encoding="utf-8", errors="replace").strip()

    if path.suffix.lower() == ".json":
        data = json.loads(text)
        return _frame_from_dict(data, meta_extra={"_format": "json", "_path": str(path)})

    # default: markdown
    meta, body = _parse_frontmatter(text)
    data: Dict[str, Any] = dict(meta)
    data.setdefault("content", body)
    return _frame_from_dict(data, meta_extra={"_format": "md", "_path": str(path)})


def _frame_from_dict(data: Dict[str, Any], meta_extra: Optional[Dict[str, Any]] = None) -> Frame:
    meta = dict(data)
    if meta_extra:
        meta.update(meta_extra)

    fid = str(data.get("id", "unknown")).strip()
    status = str(data.get("status", "undefined")).strip()
    created_utc = str(data.get("created_utc", "") or data.get("timestamp_utc", "") or "UNKNOWN_UTC").strip()
    source = str(data.get("source", "unknown")).strip()
    content = str(data.get("content", "")).strip()

    return Frame(
        id=fid,
        status=status,
        created_utc=created_utc,
        source=source,
        content=content,
        meta=meta,
    )


# -----------------------------
# Renderers (density levels)
# -----------------------------

def render(frame: Frame, density: int = 2) -> str:
    """
    density:
      1 = RAW-ish (meta + content)
      2 = Standard (id/status/time/source + content)
      3 = Max compression (id + content only)
    """
    density = int(density)

    if density <= 1:
        lines = []
        lines.append("FRAME (RAW)")
        for k in sorted(frame.meta.keys()):
            lines.append(f"{k}: {frame.meta[k]}")
        lines.append("")
        lines.append(frame.content)
        return "\n".join(lines).strip()

    if density == 3:
        return f"{frame.id}\n\n{frame.content}".strip()

    # density 2 default
    lines = []
    lines.append(f"Frame ID: {frame.id}")
    lines.append(f"Status:   {frame.status}")
    lines.append(f"UTC:      {frame.created_utc}")
    lines.append(f"Source:   {frame.source}")
    lines.append("")
    lines.append(frame.content)
    return "\n".join(lines).strip()


# -----------------------------
# Convenience
# -----------------------------

def translate_file(frame_path: str, density: int = 2) -> str:
    frame = load_frame(Path(frame_path))
    return render(frame, density=density)


# No execution on import.
# Optional CLI (explicit only):
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="eArc Nano Translator (read-only)")
    p.add_argument("path", help="Path to frame (.md or .json)")
    p.add_argument("--density", type=int, default=2, choices=[1, 2, 3], help="Render density (1/2/3)")
    args = p.parse_args()

    print(translate_file(args.path, density=args.density))
