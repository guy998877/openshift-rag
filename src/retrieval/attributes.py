"""Parse OpenShift AsciiDoc attributes from common-attributes.adoc."""
import re
from pathlib import Path

from core.config import HARDCODED_ATTRS

_ATTR_LINE = re.compile(r"^:([^:]+):\s*(.*)")
_IFDEF_ORIGIN = re.compile(r"^ifdef::openshift-origin\[\]")
_ENDIF = re.compile(r"^endif::")


def load(docs_root: Path) -> dict[str, str]:
    attrs_file = docs_root / "_attributes" / "common-attributes.adoc"
    raw: dict[str, str] = dict(HARDCODED_ATTRS)

    if attrs_file.exists():
        _parse_file(attrs_file, raw)

    # Resolve nested references up to 5 passes
    for _ in range(5):
        changed = False
        for key, val in raw.items():
            resolved = _resolve(val, raw)
            if resolved != val:
                raw[key] = resolved
                changed = True
        if not changed:
            break

    return raw


def _parse_file(path: Path, attrs: dict[str, str]) -> None:
    in_origin_block = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if _IFDEF_ORIGIN.match(line):
            in_origin_block = True
            continue
        if _ENDIF.match(line):
            in_origin_block = False
            continue
        if in_origin_block:
            continue
        m = _ATTR_LINE.match(line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            attrs[key] = val


def _resolve(val: str, attrs: dict[str, str]) -> str:
    def replacer(m: re.Match) -> str:
        name = m.group(1)
        return attrs.get(name, m.group(0))
    return re.sub(r"\{([^}]+)\}", replacer, val)


def resolve_text(text: str, attrs: dict[str, str]) -> str:
    """Resolve all {attr} references in a text string."""
    prev = None
    for _ in range(5):
        if text == prev:
            break
        prev = text
        text = _resolve(text, attrs)
    return text
