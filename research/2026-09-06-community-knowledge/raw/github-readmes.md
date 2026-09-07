===== blussyya/sldprt-format-research
# SLDPRT Reverse-Engineering Research

This is a research project to recover the serialization grammar of the SolidWorks SLDPRT binary format — syntax before semantics, never guessing meanings.

This is **not** a production converter. The old converter code (`src/`, `test/`) was removed in v0.4.0 to focus purely on format research. The goal is to understand the format well enough to build a read-only parser.

kinda vibecoded but i dont really wanna spend months working on it so agents saving me rn
dump of all the progress is [right here](https://github.com/blussyya/sldprt-research-dump "just all the files produced and used for this project all in once place")
## Knowledge Base

The project-wide knowledge base is maintained under `knowledge/`:

| File | Purpose |
|------|---------|
| `KNOWN_INVARIANTS.md` | Verified structural properties demonstrated across the corpus |
| `EXPERIMENT_LOG.md` | Ledger of every experiment with facts, hypotheses, and confidence |
| `FAILED_HYPOTHESES.md` | Hypotheses that have been disproven |
| `OPEN_QUESTIONS.md` | Broad unresolved questions |
| `NEXT_QUESTIONS.md` | Concrete operational research queue |
| `ASSUMPTIONS.md` | Working assumptions |
|# SLDPRT Reverse-Engineering Research

This is a research project to recover the serialization grammar of the SolidWorks SLDPRT binary format — syntax before semantics, never guessing meanings.

This is **not** a production converter. The old converter code (`src/`, `test/`) was removed in v0.4.0 to focus purely on format research. The goal is to understand the format well enough to build a read-only parser.

kinda vibecoded but i dont really wanna spend months working on it so agents saving me rn
dump of all the progress is [right here](https://github.com/blussyya/sldprt-research-dump "just all the files produced and used for this project all in once place")
## Knowledge Base

The project-wide knowledge base is maintained under `knowledge/`:

| File | Purpose |
|------|---------|
| `KNOWN_INVARIANTS.md` | Verified structural properties demonstrated across the corpus |
| `EXPERIMENT_LOG.md` | Ledger of every experiment with facts, hypotheses, and confidence |
| `FAILED_HYPOTHESES.md` | Hypotheses that have been disproven |
| `OPEN_QUESTIONS.md` | Broad unresolved questions |
| `NEXT_QUESTIONS.md` | Concrete operational research queue |
| `ASSUMPTIONS.md` | Working assumptions |
| `FORMAT_TIMELINE.md` | Version and container observations |
| `EVIDENCE_PRESERVATION_POLICY.md` | Rules for reproducible evidence |
| `evidence/` | Archived raw experiment outputs |
| `RESEARCH_DASHBOARD.md` | Current research posture |

## Research Versions

| Version | Description |
|---------|-------------|
| v0.3.5 | Evidence preservation policy, knowledge base restructuring, evidence archive
===== khoanguyen-3fc/ps-parser
# ps-parser

A dynamic, schema-aware library for **Parasolid XT** binary part files (`.x_b`).

The library reads the XT binary node stream against a base schema and resolves
per-node schemas on the fly — handling files that embed full or delta schema
definitions for node types that differ from (or extend) the base schema. It
also supports writing edited documents back through the library API.

## Installation

No third-party dependencies — Python 3.10+ and the standard library only.

```bash
git clone https://github.com/khoanguyen-3fc/ps-parser.git
cd ps-parser
```

## Usage

```bash
# Default: emit the node list as JSON Lines (one object per line) to stdout
python cli.py samples/model.x_b

# Dump everything: full decoded fields per node on stdout,
# parser diagnostics on stderr
python cli.py --debug samples/model.x_b

# Use a different base schema
python cli.py --schema assets/sch_13006.s_t samples/model.x_b

# Display the topology tree
python cli.py --tree samples/model.x_b
```

### Output

- **Default** — one JSON Lines object per node with all decoded fields.
- **`--debug`** — same JSON Lines output, plus detailed parser diagnostics
  (header, schema resolution, per-fie# ps-parser

A dynamic, schema-aware library for **Parasolid XT** binary part files (`.x_b`).

The library reads the XT binary node stream against a base schema and resolves
per-node schemas on the fly — handling files that embed full or delta schema
definitions for node types that differ from (or extend) the base schema. It
also supports writing edited documents back through the library API.

## Installation

No third-party dependencies — Python 3.10+ and the standard library only.

```bash
git clone https://github.com/khoanguyen-3fc/ps-parser.git
cd ps-parser
```

## Usage

```bash
# Default: emit the node list as JSON Lines (one object per line) to stdout
python cli.py samples/model.x_b

# Dump everything: full decoded fields per node on stdout,
# parser diagnostics on stderr
python cli.py --debug samples/model.x_b

# Use a different base schema
python cli.py --schema assets/sch_13006.s_t samples/model.x_b

# Display the topology tree
python cli.py --tree samples/model.x_b
```

### Output

- **Default** — one JSON Lines object per node with all decoded fields.
- **`--debug`** — same JSON Lines output, plus detailed parser diagnostics
  (header, schema resolution, per-field values) written to **stderr**.
- **`--tree`** — ASCII topology tree to stdout. Nodes are
  placed using type-specific parent pointers (`SHELL→body`, `FACE→shell`,
  `LOOP→face`, etc.). A count of nodes with unrecognized types is written to
  stderr.

Because the default output is JSON Lines, it composes with standard tools:

```bash
python cli.py samples/model.x_b | head -1 | python -m 
===== deGravity/verisolid
404: Not Found404: Not Found
===== monozukuri-ai/parasolid-kit
# parasolid-kit

`parasolid-kit` is an experimental, schema-aware parser for Parasolid X_T and
X_B transmit files. Parsing and geometry mapping run in a safe Rust core, while
Python users work with immutable typed models.

The project is read-focused and currently pre-alpha. It is intended for file
inspection, validation, research, and conversion pipelines where preserving
the transmitted structure matters more than silently approximating unsupported
data.

## Features

- Inspect X_T and X_B headers without a schema catalog.
- Parse the verified Onshape V30 subset without an external schema file.
- Use an explicit schema provider for inputs outside the built-in profile.
- Reconstruct an unmodified parsed X_B document byte-for-byte.
- Compare X_T and X_B documents after pointer-index remapping.
- Map supported topology, analytic geometry, and NURBS records to a typed B-Rep
  source model.
- Parse, map, and summarize one file with `read_brep()` or the human-readable
  `check` command.
- Convert the exact optional OCCT subset and export validated AP242 plus a
  provenance sidecar without routing through CadQuery.
- Wrap the same strict conversion as CadQuery `Shape` values for immedia# parasolid-kit

`parasolid-kit` is an experimental, schema-aware parser for Parasolid X_T and
X_B transmit files. Parsing and geometry mapping run in a safe Rust core, while
Python users work with immutable typed models.

The project is read-focused and currently pre-alpha. It is intended for file
inspection, validation, research, and conversion pipelines where preserving
the transmitted structure matters more than silently approximating unsupported
data.

## Features

- Inspect X_T and X_B headers without a schema catalog.
- Parse the verified Onshape V30 subset without an external schema file.
- Use an explicit schema provider for inputs outside the built-in profile.
- Reconstruct an unmodified parsed X_B document byte-for-byte.
- Compare X_T and X_B documents after pointer-index remapping.
- Map supported topology, analytic geometry, and NURBS records to a typed B-Rep
  source model.
- Parse, map, and summarize one file with `read_brep()` or the human-readable
  `check` command.
- Convert the exact optional OCCT subset and export validated AP242 plus a
  provenance sidecar without routing through CadQuery.
- Wrap the same strict conversion as CadQuery `Shape` values for immediate
  inspection and downstream CadQuery operations.
- Write a bounded GLB/source manifest and inspect faces or edges in a bundled,
  offline local WebGL viewer.
- Return structured diagnostics and enforce configurable resource limits.
- Use the same functionality from Python or a command-line interface with
  deterministic JSON output where required.

See [format support and limitations](docs/form
===== BlinkingSun/sldprt2step
# sldprt2step

Convert **`.SLDPRT`** part files to **ISO 10303-21 (STEP AP214)** solid
B-reps — without the CAD application that wrote them, without a CAD kernel,
and without leaving the machine.

Pure Python 3.9+, **standard library only**. Nothing to compile, no binaries,
no third-party packages, no network access. It runs on a stock system
`python3` (including macOS's `/usr/bin/python3`, 3.9.6) with no
`site-packages` at all.

```
python3 sldprt2step.py part.SLDPRT -o part.step
```

## What it actually does

It is a real **Parasolid XT neutral-binary reader**, not a mesh dump or a
preview extractor.

1. Parses the `.SLDPRT` [MS-CFB] OLE Structured Storage container and locates
   the SolidWorks 3D partition holding the geometry stream.
2. Decompresses and parses the embedded Parasolid XT transmit (base schema
   `SCH_13006` plus the embedded edit scripts).
3. Walks the B-rep topology — `BODY → REGION → SHELL → FACE → LOOP → FIN →
   EDGE → VERTEX` — and emits `MANIFOLD_SOLID_BREP` / `BREP_WITH_VOIDS` solids
   built from `ADVANCED_FACE`s.

Analytic geometry is mapped **exactly**: plane, cylinder, cone, sphere, torus,
B-spline surface, swept, spun and offset s# sldprt2step

Convert **`.SLDPRT`** part files to **ISO 10303-21 (STEP AP214)** solid
B-reps — without the CAD application that wrote them, without a CAD kernel,
and without leaving the machine.

Pure Python 3.9+, **standard library only**. Nothing to compile, no binaries,
no third-party packages, no network access. It runs on a stock system
`python3` (including macOS's `/usr/bin/python3`, 3.9.6) with no
`site-packages` at all.

```
python3 sldprt2step.py part.SLDPRT -o part.step
```

## What it actually does

It is a real **Parasolid XT neutral-binary reader**, not a mesh dump or a
preview extractor.

1. Parses the `.SLDPRT` [MS-CFB] OLE Structured Storage container and locates
   the SolidWorks 3D partition holding the geometry stream.
2. Decompresses and parses the embedded Parasolid XT transmit (base schema
   `SCH_13006` plus the embedded edit scripts).
3. Walks the B-rep topology — `BODY → REGION → SHELL → FACE → LOOP → FIN →
   EDGE → VERTEX` — and emits `MANIFOLD_SOLID_BREP` / `BREP_WITH_VOIDS` solids
   built from `ADVANCED_FACE`s.

Analytic geometry is mapped **exactly**: plane, cylinder, cone, sphere, torus,
B-spline surface, swept, spun and offset surfaces; line, circle, ellipse and
B-spline curves. Geometry that STEP cannot represent exactly — surface/surface
intersection curves, SP curves, rolling-ball blends — is approximated by
interpolating B-splines through the XT chart points, and every approximation is
reported in `warnings`.

Output is deterministic: no timestamp is written, so the same input always
produces byte-identical STEP.
