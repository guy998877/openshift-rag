"""Discover modules referenced by assemblies in TARGET_DIRS."""
import re
from dataclasses import dataclass, field
from pathlib import Path

from ingest.config import KEEP_CONTENT_TYPES, TARGET_DIRS

_INCLUDE_RE = re.compile(r"^include::(?:\.\./)*modules/([^[]+\.adoc)")
_CONTENT_TYPE_RE = re.compile(r"^:_mod-docs-content-type:\s*(\S+)")


@dataclass
class ModuleInfo:
    path: Path
    filename: str
    content_type: str
    source_dirs: list[str] = field(default_factory=list)
    topic: str = ""


def discover(
    docs_root: Path,
    target_dirs: list[str] | None = None,
    content_types: set[str] | None = None,
) -> list[ModuleInfo]:
    if target_dirs is None:
        target_dirs = TARGET_DIRS
    if content_types is None:
        content_types = KEEP_CONTENT_TYPES

    modules_dir = docs_root / "modules"
    if not modules_dir.exists():
        raise FileNotFoundError(f"modules dir not found: {modules_dir}")

    # filename -> list of source dirs that include it
    filename_to_dirs: dict[str, list[str]] = {}

    for rel_dir in target_dirs:
        asm_dir = docs_root / rel_dir
        if not asm_dir.exists():
            continue
        for asm_file in asm_dir.rglob("*.adoc"):
            try:
                text = asm_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for line in text.splitlines():
                m = _INCLUDE_RE.match(line.strip())
                if m:
                    fname = m.group(1)
                    filename_to_dirs.setdefault(fname, [])
                    if rel_dir not in filename_to_dirs[fname]:
                        filename_to_dirs[fname].append(rel_dir)

    results: list[ModuleInfo] = []
    for fname, src_dirs in filename_to_dirs.items():
        mod_path = modules_dir / fname
        if not mod_path.exists():
            continue
        content_type = _get_content_type(mod_path)
        if content_type not in content_types:
            continue
        topic = src_dirs[0].split("/")[0] if src_dirs else ""
        results.append(ModuleInfo(
            path=mod_path,
            filename=fname,
            content_type=content_type,
            source_dirs=src_dirs,
            topic=topic,
        ))

    return results


def _get_content_type(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:20]
    except OSError:
        return ""
    for line in lines:
        m = _CONTENT_TYPE_RE.match(line.strip())
        if m:
            return m.group(1).upper()
    return ""
