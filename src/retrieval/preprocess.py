"""Convert AsciiDoc modules to clean Markdown for embedding."""
import re
from pathlib import Path

from retrieval.attributes import resolve_text

# Flags for conditional processing
OCP_FLAGS: set[str] = {"openshift-enterprise"}
STRIP_FLAGS: set[str] = {
    "openshift-rosa",
    "openshift-rosa-hcp",
    "openshift-dedicated",
    "openshift-origin",
    "microshift",
}

_METADATA_PATTERNS = [
    re.compile(r"^:_mod-docs-content-type:.*"),
    re.compile(r'^\[id="[^"]*"\]'),
    re.compile(r"^include::"),
    re.compile(r"^:context:"),
    re.compile(r"^toc::\[\]"),
]

_ROLE_LINE = re.compile(r'^\[role="[^"]*"\]$')
_DISCRETE_BLOCK = re.compile(r'^\[(discrete|%collapsible|%header|colophon)[^\]]*\]$')

_IFDEF_RE = re.compile(r"^(ifdef|ifndef)::(.*)\[\]$")
_ENDIF_RE = re.compile(r"^endif::\S*\[\]$|^endif::\[\]$")
_IFEVAL_RE = re.compile(r"^ifeval::\[")
_BLOCK_OPEN = re.compile(r"^====$")  # for admonition/ifdef blocks

_ADMONITION_START = re.compile(r"^\[(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]$")
_SOURCE_BLOCK_START = re.compile(r"^\[source(?:,([^\]]*))?\]$")
_BLOCK_DELIM = re.compile(r"^([-=]{4,})$")
_HEADING_RE = re.compile(r"^(=+)\s+(.*)")
_XREF_RE = re.compile(r"xref:[^[]*\[([^\]]*)\]")
_LINK_RE = re.compile(r"link:(https?://[^[]+)\[([^\]]*)\]")
_PASS_RE = re.compile(r"pass:quotes\[([^\]]*)\]")
_LIST_ORDERED_RE = re.compile(r"^\. (.+)")
_LIST_UNORDERED_RE = re.compile(r"^\*+ (.+)")


def preprocess(path: Path, attrs: dict) -> tuple[str, str]:
    """Return (title, markdown). Raises ValueError if output too short."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # Strip leading comment block (assembly include list)
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("//"):
            start = i + 1
        else:
            break
    lines = lines[start:]

    lines = _process_conditionals(lines)
    lines = _resolve_attrs(lines, attrs)
    lines = _convert_markup(lines)
    lines = _collapse_blanks(lines)

    result = "\n".join(lines).strip()
    if len(result) < 50:
        raise ValueError("output too short (likely ROSA-only content)")

    title = _extract_title(result)
    return title, result


def _process_conditionals(lines: list[str]) -> list[str]:
    """Line-by-line state machine for ifdef/ifndef/ifeval blocks."""
    out: list[str] = []
    # Stack of booleans: True = emit lines
    stack: list[bool] = [True]
    # Flags set by ifeval blocks that we strip
    ifeval_flags: set[str] = set()
    in_ifeval = False
    ifeval_depth = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # Handle ifeval blocks — strip entirely
        if _IFEVAL_RE.match(line):
            in_ifeval = True
            ifeval_depth = 1
            i += 1
            continue

        if in_ifeval:
            # Collect any :flag: set inside ifeval
            m = re.match(r"^:([^:]+):$", line)
            if m:
                ifeval_flags.add(m.group(1))
            if line.strip() == "endif::[]" or re.match(r"^endif::", line):
                ifeval_depth -= 1
                if ifeval_depth <= 0:
                    in_ifeval = False
                    ifeval_depth = 0
            elif _IFEVAL_RE.match(line) or _IFDEF_RE.match(line):
                ifeval_depth += 1
            i += 1
            continue

        m = _IFDEF_RE.match(line)
        if m:
            directive = m.group(1)  # "ifdef" or "ifndef"
            spec = m.group(2)
            flags = {f.strip() for f in re.split(r"[,+]", spec) if f.strip()}

            # Strip ifdef for ifeval-activated flags (cloud-specific)
            if flags & ifeval_flags:
                keep = False
            elif directive == "ifdef":
                if flags & STRIP_FLAGS:
                    keep = False
                elif flags & OCP_FLAGS:
                    keep = True
                else:
                    keep = True  # unknown flag: keep conservatively
            else:  # ifndef
                if flags & STRIP_FLAGS:
                    keep = True  # ifndef::rosa = OCP content
                elif flags & OCP_FLAGS:
                    keep = False
                else:
                    keep = True

            stack.append(keep)
            i += 1
            continue

        if _ENDIF_RE.match(line):
            if len(stack) > 1:
                stack.pop()
            i += 1
            continue

        if stack[-1]:
            out.append(line)
        i += 1

    return out


def _resolve_attrs(lines: list[str], attrs: dict) -> list[str]:
    return [resolve_text(line, attrs) for line in lines]


def _convert_markup(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Strip metadata lines
        if any(p.match(line) for p in _METADATA_PATTERNS):
            i += 1
            continue

        # Strip role annotations
        if _ROLE_LINE.match(line):
            i += 1
            continue

        # Strip standalone block attributes like [discrete], [%collapsible]
        if _DISCRETE_BLOCK.match(line):
            i += 1
            continue

        # Admonition blocks: [NOTE]\n====\n...\n====
        m = _ADMONITION_START.match(line)
        if m:
            kind = m.group(1)
            i += 1
            # Consume opening delimiter
            if i < len(lines) and _BLOCK_OPEN.match(lines[i]):
                i += 1
            block_lines: list[str] = []
            while i < len(lines) and not _BLOCK_OPEN.match(lines[i]):
                block_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # consume closing ====
            block_text = " ".join(l.strip() for l in block_lines if l.strip())
            out.append(f"> **{kind}:** {block_text}")
            continue

        # Source/code blocks
        m = _SOURCE_BLOCK_START.match(line)
        if m:
            lang_spec = (m.group(1) or "").strip().lower()
            lang = _map_lang(lang_spec)
            i += 1
            # Consume opening ----
            if i < len(lines) and _BLOCK_DELIM.match(lines[i]):
                i += 1
            code_lines: list[str] = []
            while i < len(lines) and not _BLOCK_DELIM.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # consume closing ----
            out.append(f"```{lang}")
            out.extend(code_lines)
            out.append("```")
            continue

        # Bare ---- delimiters (unlabeled blocks) — strip
        if _BLOCK_DELIM.match(line):
            i += 1
            continue

        # Headings
        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            out.append("#" * level + " " + title)
            i += 1
            continue

        # List continuation lines
        if line.strip() == "+":
            i += 1
            continue

        # Ordered list: ". item"
        m = _LIST_ORDERED_RE.match(line)
        if m:
            out.append("1. " + m.group(1))
            i += 1
            continue

        # Unordered list: "* item" or "** item"
        m = _LIST_UNORDERED_RE.match(line)
        if m:
            out.append("- " + m.group(1))
            i += 1
            continue

        # Inline transformations
        line = _XREF_RE.sub(lambda x: x.group(1) or x.group(0), line)
        line = _LINK_RE.sub(lambda x: f"[{x.group(2)}]({x.group(1)})", line)
        line = _PASS_RE.sub(lambda x: x.group(1), line)

        out.append(line)
        i += 1

    return out


def _map_lang(spec: str) -> str:
    mapping = {
        "terminal": "bash",
        "yaml": "yaml",
        "json": "json",
        "xml": "xml",
        "bash": "bash",
        "sh": "bash",
        "python": "python",
        "go": "go",
    }
    # spec may be "terminal,subs=+quotes" etc.
    base = spec.split(",")[0].strip()
    return mapping.get(base, base)


def _collapse_blanks(lines: list[str]) -> list[str]:
    out: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 1:
                out.append("")
        else:
            blank_count = 0
            out.append(line)
    return out


def _extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""
