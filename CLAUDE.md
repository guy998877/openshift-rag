# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) system targeting OpenShift platform engineers, cluster admins, and SRE/DevOps users. The goal is to retrieve version-correct, task-oriented answers from the official OpenShift documentation for operational tasks: installation, upgrades, operators, and troubleshooting.

- **Python**: >=3.13, managed with `uv`
- **Key dependency**: `openai>=2.29.0`
- **Documentation corpus**: `openshift-docs/` (~11,126 AsciiDoc files, 1.5GB)

## Environment Setup

```bash
uv sync          # install dependencies into .venv
source .venv/bin/activate
```

## Documentation Corpus Architecture (`openshift-docs/`)

The docs follow a strict **assembly → module → snippet** inclusion model:

- **Assemblies** (topic-level `.adoc` files): top-level containers that `include::` modules. Located in topic directories (`installing/`, `operators/`, `networking/`, etc.)
- **`modules/`** (8,394 files): the reusable content atoms — the primary text unit to index for RAG.
- **`snippets/`** (342 files): short text fragments included by modules.

Each file declares its type via `:_mod-docs-content-type:` (ASSEMBLY, CONCEPT, PROCEDURE, REFERENCE, SNIPPET).

### Key Structural Files

| File | Purpose |
|---|---|
| `_distro_map.yml` | Maps distributions (OCP, OKD, OSD, ROSA, MicroShift) and version branches (3.6–4.21) |
| `_topic_maps/*.yml` | Navigation structure per distribution |
| `_attributes/common-attributes.adoc` | Global AsciiDoc attributes (`{product-title}`, `{context}`, etc.) |
| `api-config.yaml` | Defines which Kubernetes/OpenShift API resources get documented |

### Content Variants

Five major product distributions share the same source files with conditional content (`ifdef`/`ifndef`/`ifeval` directives):
- **OCP** — OpenShift Container Platform (enterprise)
- **OKD** — Community upstream
- **OSD** — OpenShift Dedicated
- **ROSA** — Red Hat OpenShift Service on AWS (including ROSA HCP)
- **MicroShift** — Edge/embedded variant

Topic directories prefixed with `rosa_`, `microshift_`, or `osd_` are distribution-specific.

### RAG Indexing Guidance

- **Index `modules/` files** as the primary content unit — they contain the actual procedural and conceptual text.
- **Assemblies** provide context (which modules belong together) but are largely structural includes.
- **Resolve AsciiDoc attributes** before indexing: replace `{product-title}`, `{context}`, etc. using values from `_attributes/common-attributes.adoc`.
- **Handle conditional blocks**: `ifdef::openshift-enterprise[]` ... `endif::[]` — decide which distribution context to resolve for.
- **Cross-references** use `xref:` and `link:` syntax; these can be used to build a document graph.
- **Images** (PNG/SVG in `images/`) are supplementary — diagrams and screenshots.

### Build Scripts (inside `openshift-docs/`)

These operate on the docs corpus itself — not part of the RAG pipeline:

```bash
python build.py                  # validate AsciiDoc → HTML conversion
python build_for_portal.py       # portal-targeted build output
bash scripts/check-with-vale.sh  # style/grammar linting via Vale
bash scripts/check-asciidoctor-build.sh  # validate compilation
```
