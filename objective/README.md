# objective

**Relational domain adaptation via verifiable data products, model-independent oracles, independent judges, and a bespoke hierarchical sequence model trained from scratch.**

This repository (`sdg-strategy`) is one of two sibling **data products** that make the cross-project "Signals" programme reproducible, auditable, and portable. The other is `sdg-corpora`.

## Programme Thesis

The Signals programme (of which Aegir is the relational domain-adaptation workstream) rests on three commitments:

1. **The ontology is the primary, model-independent domain surface.**  
   A de-novo-curated, reasoner-verified ontology (BFO 2020 + CCO grounded) carries domain meaning independently of any learned model. It can be evolved before a trusted model exists.

2. **The reasoner (HermiT) is the model-independent formal oracle.**  
   Sound and complete. It certifies *formal* correctness (consistency, realization, membrane admission). The corpus and (future) model certify *domain* correctness. These anchors remain distinct.

3. **The H-Net+RWKV model (trained from scratch) is the ultimate domain-adapted fitness measure.**  
   Trained on the ontology-grounded relational corpus. It is deliberately kept as a trustworthy, non-co-adapting arbiter for relational understanding and *de novo* Data Element elucidation. The upstream generator (instrumented models used during corpus creation) and the downstream bespoke model are kept distinct.

Everything else — Atlas glossary, Qdrant lenses, build projections, the lineup, published releases, agent harnesses, classification runs — are **projections, indices, or consumers** of the ontology + corpus + strategy.

## The Two Data Products

### sdg-corpora (the "what" / SHARE tier)

Pinned as a git submodule in consumers (`corpora/` in Aegir, `external/sdg-corpora/` in Atelier).

Contains the published, attribution-clean artifacts:

- `ontology/` — `sdg-ontology.owl` / `.omn`, family catalogs (01–08), `HERMIT_CERTIFICATE.md`, `SLOT_DSL.md`.
- `vocabulary/annotations.{parquet,csv}` + `vocabulary.ttl` — the SKOS ConceptScheme + ReferenceCategory-shaped annotations (code, label, parent_code, domain_hypernym hints, example_values, etc.). This is the classification vocabulary.
- `ddl/<run_id>/` — relational footprint as parquet: `base_rows`, `base_table_index`, `cross_family_fks`, `ddl_statements` (with ground-truth JSON in SQL `COMMENT`s), views, validation artifacts.
- `corpus/collections/` — topic-grounded chapters with RI-true tables woven in.

Releases are produced by `aegir.lineup sync` (gated by schema-CI + OQuaRE) and `build_atelier_release.py`.

**Atelier contract**: A tagged release supplies the blind data source. Reference codes (column → semantic type) are withheld. Atelier classifies; Aegir scores.

### sdg-strategy (the "how" / determinants)

This repository. A content-addressed, Merkle-shaped record of every outcome-shaping factor that is *neither* the raw input window (FinePDFs harvest cursor + passages) *nor* the code commit.

A run is determined by the **provenance triple** `(window, strategy, code)`.

`strategy_id` is the root identity. Release tags and zettel identifiers are names.

## sdg-strategy Architecture

### Identity

```python
strategy_id = sha256( json.dumps(sorted(component_hashes), sort_keys=True) )[:12]
```

- Verifiable by rehash from *any* signals project (Atelier, Gaius, future) with no Aegir context.
- `manifests/<strategy_id>.json` is the Merkle tree.
- `CURRENT` names the checked-out strategy on the main lineage.
- Component paths are the leaves (e.g. `lens/vocab.snapshot.json`, `voices/derive.system.md`).

Example manifest (truncated):

```json
{
  "strategy_id": "7e573f054e16",
  "components": {
    "lens/aiming.snapshot.json": "df555358e4a7eddc...",
    "lens/binding.json": "cf71372769c1...",
    ...
    "voices/aegir_writer.md": "8f02bfcb7dd4...",
    "targets/schemapile_shape_norms.json": "4000c3fc9f8c..."
  },
  "pillars": {
    "lens": ["lens/aiming.skos.ttl", "lens/aiming.snapshot.json", ...],
    "voices": ["voices/derive.system.md", "voices/derive.schema.json", ...],
    "knobs": ["knobs/flow_defaults.json"],
    "targets": ["targets/brand_lexicon.json", ...]
  }
}
```

### The Four Pillars (verbatim capture)

| Pillar   | Contents | Captured by |
|----------|----------|-------------|
| `lens/`  | Qdrant snapshots (aiming + full vocab), SKOS sources (vocab + aiming), `binding.json` (collection names + qdrant_url + materialized_from) | `collect_lens()` — scrolls live collections, reads TTL sources, declares the runtime targets |
| `voices/` | Every agent-facing surface: system prompts, schemas, feedback functions (source), dormant hints, register_voice, turn protocols, backend TOML, MCP tool docstrings (via AST), vendored `aegir_writer.md` | `collect_voices()` — imports + inspect + AST walk of tool decorators |
| `knobs/` | Flow Parameter defaults (read from Metaflow class, not literals) | `collect_knobs()` — reflects `SdgCorporaFlow` Parameters |
| `targets/` | SchemaPile mined norms (key + shape), brand lexicon patterns, gate floors (payload_min_chars, verdict_accept, etc.) | `collect_targets()` — reads build artifacts + code constants |

Truth direction is **repo → runtime**. The live Qdrant collection is materialized *from* the SKOS in the strategy (see `materialize.py`). Code follows the declared binding.

### Main Lineage vs. Shadows

- **trunk** is the one-main invariant. Only trunk receives release tags.
- A **shadow** is a branch from a trunk@sha. Shared ancestry is the branch point; diff is ordinary `git diff`.
- Promotion = cherry-pick (entry level) or merge.
- Consumers never assume a working tree for shadows.

### Resolution and Pinning (the key seam)

In Aegir:

```python
# One environment variable routes everything
os.environ["AEGIR_STRATEGY_REF"] = "some-branch-or-sha"

man = declared()                    # CURRENT or load_by_ref(AEGIR_STRATEGY_REF)
binding = lens_binding(ref)         # reads components/... via git show when ref given
component = read_component(path, ref)  # working tree or `git show ref:components/...`
```

Core functions (`src/aegir/strategy/manifest.py`):

- `collect()` → (components dict of path→bytes, manifest)
- `write_to_submodule(...)` — seeds components/ + manifests/ + CURRENT
- `declared()` — follows env var or CURRENT
- `load_by_ref(ref)` — `git show {ref}:CURRENT` + `git show {ref}:manifests/{sid}.json`
- `read_component(path, ref=None)`
- `drift(manifest)` — live vs declared (used with optional hard `AEGIR_STRATEGY_ENFORCE=1`)
- `submodule_commit()`

### Lineage and Cache Keys (`strategy/lineage.py`)

```python
STAGE_INPUTS = {
    "harvest": ["lens/"],
    "derive": ["lens/", "voices/derive.system.md", ...],
    "realize": ["targets/schemapile_shape_norms.json"],
    ...
}

def stage_key(stage, manifest): ...
def span_facets(stage, manifest): ...   # OpenLineage-shaped OTel attributes
```

These keys are recorded in run zettels and used for impact analysis / cache invalidation.

### Materialization (`strategy/materialize.py`)

```bash
uv run --no-sync python -m aegir.strategy.materialize <ref> [--force]
```

Rebuilds the aiming and vocab Qdrant collections from the strategy's SKOS + binding. Verifies point counts against the captured snapshots. Enables a shadow branch to become runnable with one command.

## Producer (Aegir) × Judge (Atelier) Contract

**Aegir** (producer):
- Runs the full pipeline: harvest → metrology-informed derive (agent + SchemaPile/kvasir feedback) → HermiT realization → constructs → parallel prose harnesses.
- Seeds strategy on main (or per-shadow).
- Produces sdg-corpora releases (gated).
- Will train the H-Net+RWKV model from scratch on the resulting substrate.
- Scores both its own and Atelier's predictions against the withheld reference.

**Atelier** (independent judge + classification workbench):
- Pins a specific sdg-corpora release via submodule.
- Reconstructs blind columns from `ddl/.../base_rows.parquet` + vocabulary.
- Runs its own classification pipelines (multiple families: classical, embedding, agent-mediated, etc.).
- Produces predictions + rich audit/scoring artifacts.
- Does **not** see the reference codes during the blind phase.
- Also serves as a full agentic workbench (gRPC + React + embedding atlas + overwatch + referee).

The lift question is explicit:

> Aegir-RWKV (or H-Net+RWKV) + metrology − Atelier (strong independent baseline on identical held-out columns) = the bespoke model's real value-add.

This is why the generator used during corpus creation and the final bespoke model are kept distinct.

## The Bespoke Model (Aegir)

Defined in `src/aegir/models/` and `src/aegir/modules/`:

```python
class Aegir(nn.Module):
    """Recursive hierarchical sequence model.
    Combines RWKV-8 (with ROSA) at the innermost stage with Mamba-2
    encoder/decoder at outer stages, connected by content-dependent
    dynamic chunking.

    Adapted from H-Net (goombalab/hnet), with RWKV-8 block type support.
    """
```

Architecture layout is recursive (example):

```python
arch_layout = ["m4", ["m4", ["r12"], "m4"], "m4"]   # outer Mamba → ... → inner RWKV
```

- Outer stages: high-resolution, dynamic routing + chunking (content-dependent segmentation).
- Inner stage: operates over learned semantic chunks with a strong recurrent model (RWKV family).
- Heads (`models/heads.py`):
  - `AegirForCausalLM` (pretraining / generation)
  - `AegirForColumnAnnotation` (CTA/CPA — exactly the tasks Atelier measures)
  - `DEDOutput` (cross-table data element discovery embeddings)

Training infrastructure includes continued pretrain flows, custom fused kernels (RWKV-7/8 TimeMix), table-aware datasets, and synthetic data generation.

**Why H-Net + RWKV fits this domain**:
- Relational data + column values + technical prose descriptions contain structure that static tokenizers destroy (mixed natural language, SQL-like, value pools, hierarchical names).
- Dynamic, data-dependent chunking aligns with the existing hierarchical structures (ontology families, BFO anchors, table→column, domain taxonomy, lens apertures).
- Byte-level / sub-token operation + hierarchy gives a path to better long-context, better structural generalization, and more sample-efficient adaptation on the generated corpus.
- RWKV provides linear-time, constant-memory recurrence suitable for the inner model operating on compressed chunks.

## Captured vs. Not-Yet-Captured Commonality

**Already extracted / portable**:
- sdg-corpora and sdg-strategy as content-addressed, git-submodule data products.
- Verifiable strategy manifests (rehashable from any project).
- Ontology + reasoner as model-independent substrate.
- Blind evaluation contract + withheld reference discipline.
- Provenance triple and stage lineage keys.
- Voice surfaces (partially) via the voices pillar.

**Still largely project-local** (opportunities for further utility extraction):
- Concrete "Relational Signal" types (column-in-context + predictions + scores + metrology verdicts).
- Reference / ground-truth management as a first-class, versioned concern (currently split across targets/, curated_reference, DDL comments, annotations).
- Full model descriptor + training strategy (data mix, H-Net stage parameters, RWKV config, curriculum) that can be cited the same way generation strategies are.
- Shared agent harness / metrology loop primitives (derive feedback, referee, overwatch patterns).
- Common embedding / retrieval / hierarchical indexing abstractions that compose with the model's dynamic chunking.
- Symmetric "strategy" support for classification runs and model training runs (so Atelier and Gaius can declare their own determinants).
- A thin, shared loading / manifest / ref-resolution library usable outside Aegir.

## Modality Bindings — the instrument generalizes; the specimens change

Nothing in the constitution, the Merkle identity, shadows-as-branches, the clearinghouse,
or the provenance triple knows about *text*. Only the **collectors** bind a modality. A
sibling programme (e.g. the cybersecurity workstream: synthetic OpenTelemetry / CloudTrail
stored as HDF5-organized Iceberg tables in object storage) reimplements the collectors and
inherits everything else. Pillar by pillar:

| pillar | text / FinePDFs binding (this repo, reference impl.) | telemetry / Iceberg binding (planned sibling) |
|---|---|---|
| **window** | harvest cursor + content-hashed passages (immutability by approximation) | **Iceberg snapshot ID + partition range** — exact, atomic, time-travelable. *This is the reference design for window pinning*; the text binding should converge toward it where its stores permit |
| **lens** | qdrant aperture (SKOS-sourced ColBERT collections) + `binding.json`; materialized repo → runtime | detector/selector sets over event streams; access-path rules (RETE-style field/partition selectors) declaring which telemetry reaches derivation |
| **voices** | derive prompts, schemas, feedback sources, tool docstrings, vendored writer profile | generator scenario configs + agent surfaces in detection/triage loops |
| **knobs** | flow parameter defaults | pipeline/job parameter defaults (Flink job configs, window sizes, rates) |
| **targets** | SchemaPile-mined structural norms, gate floors, brand lexicon | investigation-pattern norms mined from operational reality (query-shape distributions, hot-field rates, tiering policies) — the same epistemic move: *norms measured from the real workload, content-hashed* |
| **objective** | reasoning tasks in-kind over the system's own artifacts (elucidation, provenance, reverse-engineering) | investigation tasks in-kind (time-bounded reconstruction, attribution, resource forensics, anomaly explanation) — same `tasks/` + `tasks-json/` format |

Two properties transfer with special force:

1. **The producer × judge contract is native wherever generation knows its ground truth.**
   Synthetic telemetry with planted threat narratives (reference withheld) is the blind-column
   contract in another modality: the producer generates and scores; an independent judge
   detects blind. Any modality whose generator knows what it planted gets this for free.
2. **Window semantics deserve the strongest store available.** Iceberg snapshots make the
   window pillar exact rather than approximated; when a modality's substrate offers atomic,
   content-addressed windows, the strategy manifest should pin those identifiers directly.

The portability rule: **if adopting a new modality requires touching anything other than the
collectors and the task specimens, that is a defect in this repository, not in the modality.**

## Gaius and Future Extensibility

Gaius is the interactive orchestration, TUI, KB, swarm, and agent platform layer. It is expected to consume the same data products and strategy manifests for reproducibility and explanation. Future work in this repository (or sibling utility layers) may add pillars or sibling manifests to support:
- Swarm evolution / content pipeline determinants
- Interactive panel and navigation configurations that affect outcomes
- Model serving and inference configuration for the bespoke backbone
- Cross-signal composition (Aegir generations + Atelier classifications + model inferences)

The design principle remains: **make the invisible determinants explicit, content-addressed, and re-verifiable** so that any signals project can cite a precise `(window, strategy, code, model)` tuple.

## How This Repository Is Used

- **Seed**: `python -m aegir.strategy.manifest seed` (inside Aegir, with strategy/ submodule mounted)
- **Drift check**: `python -m aegir.strategy.manifest drift`
- **Shadow run**: `... --strategy <branch-or-sha>` (sets `AEGIR_STRATEGY_REF`)
- **Materialize for a ref**: `python -m aegir.strategy.materialize <ref>`
- **Consumers** read manifests and components via `declared()`, `load_by_ref()`, or direct git object access.

The `components/` tree here *is* the artifact. The manifests are the Merkle proof.

## Status and Evolution

This document lives in `objective/README.md` inside the sdg-strategy repository precisely because the programme treats cross-cutting, verifiable concerns as first-class data products rather than code that lives in only one pipeline.

The structure and pillars will evolve as support for Gaius, model training provenance, richer reference strategies, and additional signal types is required. All changes remain subject to the same identity, drift, and shadow discipline.

---

*Maintained as part of the Signals programme. See also: Aegir's `src/aegir/strategy/`, `docs/current/src/signals_programme.md`, `atelier-evals.txt`, `sdg-strat-design_01.txt`, and the corresponding documents in Atelier and Gaius.*