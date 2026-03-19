from pathlib import Path

TARGET_DIRS = [
    "support/troubleshooting",
    "upgrading",
    "operators/understanding",
    "operators/admin",
    "nodes",
    "post_installation_configuration",
    "updating",
    "machine_management",
    "machine_configuration",
    "authentication",
    "backup_and_restore",
    "architecture",
    "applications",
    "storage",
]

KEEP_CONTENT_TYPES = {"PROCEDURE", "CONCEPT"}

DEFAULT_DOCS_ROOT = Path("./openshift-docs")
DEFAULT_PROCESSED_DIR = Path("./data/processed")
DEFAULT_CHROMA_DIR = Path("./chroma_db")
DEFAULT_COLLECTION = "openshift_docs_v0"
DEFAULT_BATCH_SIZE = 100

EMBEDDING_MODEL = "text-embedding-3-small"

HARDCODED_ATTRS = {
    "product-title": "OpenShift Container Platform",
    "product-version": "4.21",
    "nbsp": " ",
    "global_ns": "openshift-operators",
    "cluster-manager": "OpenShift Cluster Manager",
    "op-system-first": "Red Hat Enterprise Linux CoreOS (RHCOS)",
}
