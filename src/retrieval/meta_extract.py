"""Extract rich metadata from preprocessed Markdown for ChromaDB storage."""
import re

from core.config import HARDCODED_ATTRS
from retrieval.discover import ModuleInfo

_CODE_FENCE_RE = re.compile(r"^```(\w+)?")
_OC_CMD_RE = re.compile(r"^\$\s+oc\s+(\S+)")

_API_RESOURCES = [
    "Pod", "Deployment", "StatefulSet", "DaemonSet", "ReplicaSet", "Job", "CronJob",
    "Node", "Namespace", "Service", "Route", "Ingress", "NetworkPolicy",
    "ConfigMap", "Secret", "ServiceAccount",
    "PersistentVolume", "PersistentVolumeClaim", "StorageClass",
    "MachineSet", "Machine", "MachineConfig", "MachineConfigPool",
    "ClusterOperator", "ClusterVersion",
    "Operator", "Subscription", "OperatorGroup", "CatalogSource", "InstallPlan",
    "CustomResourceDefinition",
    "Role", "ClusterRole", "RoleBinding", "ClusterRoleBinding",
    "LimitRange", "ResourceQuota",
]
_API_RESOURCE_RE = re.compile(
    r"\b(" + "|".join(re.escape(r) for r in _API_RESOURCES) + r")\b"
)


def extract(text: str, mod: ModuleInfo) -> dict:
    """Return a flat dict of metadata fields derived from the markdown text and ModuleInfo."""
    lines = text.splitlines()

    word_count = len(text.split())
    has_code, code_langs = _code_info(lines)
    oc_commands = _oc_commands(lines)
    api_resources = _api_resources(text)

    return {
        # Quantitative
        "word_count": word_count,
        "assembly_count": len(mod.source_dirs),
        # Code signals
        "has_code": int(has_code),
        "code_langs": code_langs,
        # Section signals
        "has_prerequisites": int(".Prerequisites" in text),
        "has_verification": int(".Verification" in text),
        "is_troubleshooting": int(
            "troubleshoot" in text.lower()
            or "support" in mod.topic
            or any("troubleshoot" in d for d in mod.source_dirs)
        ),
        # Permission signals
        "requires_cluster_admin": int("cluster-admin" in text),
        # Command signals
        "oc_commands": oc_commands,
        # Resource signals
        "api_resources": api_resources,
        # Version
        "ocp_version": HARDCODED_ATTRS["product-version"],
    }


def _code_info(lines: list[str]) -> tuple[bool, str]:
    langs: list[str] = []
    for line in lines:
        m = _CODE_FENCE_RE.match(line)
        if m and m.group(1):
            lang = m.group(1).strip()
            if lang and lang not in langs:
                langs.append(lang)
    return bool(langs), ",".join(langs)


def _oc_commands(lines: list[str]) -> str:
    cmds: list[str] = []
    for line in lines:
        m = _OC_CMD_RE.match(line.strip())
        if m:
            cmd = m.group(1)
            if cmd not in cmds:
                cmds.append(cmd)
    return ",".join(cmds)


def _api_resources(text: str) -> str:
    found: list[str] = []
    for m in _API_RESOURCE_RE.finditer(text):
        name = m.group(1)
        if name not in found:
            found.append(name)
    return ",".join(found)
