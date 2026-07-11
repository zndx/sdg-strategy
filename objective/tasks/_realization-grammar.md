# Realization Grammar (authoring extract)

**Non-normative.** Open-Reasoning-Tasks style cards are standalone: the binding
realization grammar is **inlined** in:

- `composite-grounding-recovery-from-chapters.md`

Edit that task file for export. Keep this extract in sync only as an editor
convenience when changing the shared surface.

## Forward composition

```
g : Ontology → Relational     (realization / constructs)
v : Relational → Views        (view synthesis)
p : Views (+ prose) → Chapter
```

A **witness** is a pair `(ĝ, v̂)` claimed to realize a chapter’s visible views.
Validity is **grammaticality + internal commutativity**, not identity with any
particular generator DDL.

---

## g-side — ontology → relational (licensed)

### Entity tables

| form | meaning |
|------|---------|
| **class → table** | An ontology class (or association class) may be realized as a base table. **Table naming is free** (not scored for identity). |
| **subclass** | Licensed options (pick one per witness; mark forced/free): **single-table** (discriminator or nullable subclass columns), **table-per-class** (subclass table + FK to parent). Other inheritance strategies are out of v1. |

### Properties

| form | meaning |
|------|---------|
| **datatype property → column** | On the table realizing the property’s domain class (or on an EAV value table under the EAV profile). |
| **object property → FK (direct)** | When the property is treated as functional / to-one in the profile: FK column on the source table referencing the target table’s key. |
| **object property → junction table** | When many-to-many / association-class: junction table with FKs to both ends; optional attributes on the junction. **Both direct FK and junction are legal** for non-functional relations unless the specimen pins one. |

### Identifiers

| form | meaning |
|------|---------|
| **surrogate key** | Synthetic primary key (e.g. `id`) — **artifact** relative to pure ontology content; licensed by identifier policy. |
| **natural / designative key** | Column realizing a Designative ICE / identifier datatype property may serve as PK or unique key. |

### Profiles (optional witness labels)

A witness may name a profile consistent with `grounds_ddl`-style lowering:

| profile | sketch |
|---------|--------|
| **normalized** | One primary table; properties as columns/FKs |
| **eav** | Entity + attribute registry + typed value tables + reconstruction view |
| **junction** | Association tables for n-ary / many-to-many |
| **star / snowflake** | Fact + dimensions (snowflake: normalized dimensions) |

Profile choice is typically **free** unless evidence forces structure (e.g. EAV shape in a rendered long view).

### g illegal

- FK that realizes **no** object property (and is not a licensed identifier/policy edge stated in the specimen).
- Column that realizes **no** datatype property, identifier policy, or declared artifact class.
- Junction that does not correspond to a relation/association in the frame.
- Joining tables with no path of licensed FKs in `ĝ`.

---

## v-side — relational → views (licensed)

### Operators (v1)

| operator | meaning |
|----------|---------|
| **project** | Select a subset of columns from a base table or intermediate |
| **select** | Row filter (equality / null checks as needed for specimens) |
| **rename** | Column rename in the view signature |
| **equi-join** | Join **only** on a declared FK edge in `ĝ` (PK/FK columns) |
| **aggregation** | `count`, `sum`, `avg`, `min`, `max` over a grouping (group keys must be projected columns or join keys) |
| **arithmetic** | `+`, `-`, `*`, `/` over numeric columns (e.g. `qty * unit_price`) |
| **concat** | String concatenation of columns / literals |

### View shapes commonly emitted by the pipeline

- **Projection view** — single base table, column subset (optionally renamed).
- **Join view** — two (or more, v1 specimens stick to binary) tables via FK; denormalized signature.
- **Reconstruction view** — EAV/junction/star “wide” form rebuilt for chapters (still composed of licensed ops).

### v illegal

- Join on non-key columns or on columns not licensed as an FK edge in `ĝ`.
- Operators outside the set above.
- View column with **no** route from some ontology path or declared artifact through `ĝ` then `v̂` (unless marked free-text noise and rejected).
- Using a view **body** (SQL text naming base tables) as input evidence — bodies are **withheld**; only rendered signatures + sample rows are given.

---

## Composite claims

A **composite grounding** for a view column is an ontology path:

```
Class  —objectProperty→  …  —datatypeProperty→  leaf
```

optionally with a terminal **operator** (`arith`, `agg`, `concat`) over one or more properties.

The witness must show `v̂(ĝ(path))` producing that view column (commutativity).

---

## Forced vs free (J)

A witness component is:

- **forced** — present in **all** grammar-valid factorizations consistent with the evidence (and simulator-enumerated set, when given);
- **free** — differs across at least two valid factorizations.

Examples:

- Correlated columns across a join view **force** that *some* FK edge existed; junction-vs-direct and table **names** are typically **free**.
- Surrogate `id` is often **forced as artifact** under identifier policy once a table is hypothesized, while its name is free.

---

## Artifacts and silent elements

| kind | definition |
|------|------------|
| **Artifact** | View or base column with **no** ontological referent; must still have a witness origin (surrogate PK policy, ETL timestamp, load batch id, …). |
| **Silent element** | Frame member realized by some legal `ĝ` but **projected away** by every given `v̂` — invisible in the chapter’s views. |

---

## ICE trichotomy (default coarsened frame for Q)

When leaf grounding under-determines among children, default coarsened parents:

| parent | typical leaves |
|--------|----------------|
| **DesignativeICE** | identifiers, codes used as names, surrogate-adjacent designators |
| **DescriptiveICE** | measurements, quantities, free descriptions, timestamps of occurrence |
| **PrescriptiveICE** | status codes, directives, controlled state vocabularies |

Inherit coarsened counting / projection rules from the opinion algebra (W = 2; parent mass atomic under v1).

---

## Scoring hooks (for generators / judges)

1. **Composite correctness** — view column → path (+ op) vs alignment table (set equality if multi-valued).
2. **Grammaticality** — every `ĝ`/`v̂` step ∈ this module.
3. **Internal commutativity** — witness routes agree with composite claims (**no hidden DDL required**).
4. **Forced/free** — vs enumerated or sampled factorization set (simulator fact).

v1 weights: **equal** across 1–4 (marked deliberate). Hierarchical partial credit on composite endpoints: **out of scope** (atomic coarsened elements).

---

## Expansion ledger (TODO — not v1-normative until promoted)

- [ ] Full table-per-concrete-class / shared-PK inheritance variants beyond the two subclass options
- [ ] Outer joins, window functions, CASE expressions
- [ ] Multi-way joins (>2 tables) as first-class grammar (specimens may still chain binary joins)
- [ ] Profile-forced evidence patterns per `grounds_ddl` complete matrix
- [ ] Mechanical extract tests against `realize.py` / `chapter_tables.py` CI
