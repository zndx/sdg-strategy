# Composite Grounding Recovery from Chapters

## Description:
This task requires recovering **column-level ontology groundings** for chapter-embedded **views**, together with a **relational witness** that shows how those groundings could arise — without treating any particular table DDL as the unique truth.

### Premise

Forward generation is a composition:

```
g : Ontology → Relational      (realization / constructs)
v : Relational → Views         (view synthesis)
p : Views (+ prose harness) → Chapter
```

**Identifiability:** given chapter prose plus rendered view surfaces, the factorization `(g, v)` is underdetermined — many relational realizations can mediate the same visible evidence — but the **composite** `v ∘ g`, restricted to **column-level grounding**, is recoverable (generator alignment is the ground-truth artifact).

**Resolution:** the relational middle is a **witness, not a fact** (proof-object semantics). The model must exhibit a commuting square

```
Ontology ──ĝ──▶ Relational ──v̂──▶ Views
```

and is graded on **validity of the square**, never on identity with a hidden generator DDL. Punishing valid alternative factorizations trains convention-guessing, not reasoning.

**Differentiation:** endpoint-only column→class maps without a witness are **anti-pattern (a)** — they collapse this task into blind column classification. Scored content is the **traversal** (path + operators + witness), not the leaf label alone.

### Realization grammar (normative, self-contained)

v1 licensed `ĝ` / `v̂` forms. Specimens may state deltas. Expansion items at the end of this section are non-normative until promoted.

#### Forward composition

```
g : Ontology → Relational     (realization / constructs)
v : Relational → Views        (view synthesis)
p : Views (+ prose) → Chapter
```

A **witness** is a pair `(ĝ, v̂)` claimed to realize a chapter’s visible views.
Validity is **grammaticality + internal commutativity**, not identity with any
particular generator DDL.

---

#### g-side — ontology → relational (licensed)

##### Entity tables

| form | meaning |
|------|---------|
| **class → table** | An ontology class (or association class) may be realized as a base table. **Table naming is free** (not scored for identity). |
| **subclass** | Licensed options (pick one per witness; mark forced/free): **single-table** (discriminator or nullable subclass columns), **table-per-class** (subclass table + FK to parent). Other inheritance strategies are out of v1. |

##### Properties

| form | meaning |
|------|---------|
| **datatype property → column** | On the table realizing the property’s domain class (or on an EAV value table under the EAV profile). |
| **object property → FK (direct)** | When the property is treated as functional / to-one in the profile: FK column on the source table referencing the target table’s key. |
| **object property → junction table** | When many-to-many / association-class: junction table with FKs to both ends; optional attributes on the junction. **Both direct FK and junction are legal** for non-functional relations unless the specimen pins one. |

##### Identifiers

| form | meaning |
|------|---------|
| **surrogate key** | Synthetic primary key (e.g. `id`) — **artifact** relative to pure ontology content; licensed by identifier policy. |
| **natural / designative key** | Column realizing Designative ICE (`cco:ont00000686`) / an identifier datatype property may serve as PK or unique key. |

##### Profiles (optional witness labels)

A witness may name a profile consistent with `grounds_ddl`-style lowering:

| profile | sketch |
|---------|--------|
| **normalized** | One primary table; properties as columns/FKs |
| **eav** | Entity + attribute registry + typed value tables + reconstruction view |
| **junction** | Association tables for n-ary / many-to-many |
| **star / snowflake** | Fact + dimensions (snowflake: normalized dimensions) |

Profile choice is typically **free** unless evidence forces structure (e.g. EAV shape in a rendered long view).

##### g illegal

- FK that realizes **no** object property (and is not a licensed identifier/policy edge stated in the specimen).
- Column that realizes **no** datatype property, identifier policy, or declared artifact class.
- Junction that does not correspond to a relation/association in the frame.
- Joining tables with no path of licensed FKs in `ĝ`.

---

#### v-side — relational → views (licensed)

##### Operators (v1)

| operator | meaning |
|----------|---------|
| **project** | Select a subset of columns from a base table or intermediate |
| **select** | Row filter (equality / null checks as needed for specimens) |
| **rename** | Column rename in the view signature |
| **equi-join** | Join **only** on a declared FK edge in `ĝ` (PK/FK columns) |
| **aggregation** | `count`, `sum`, `avg`, `min`, `max` over a grouping (group keys must be projected columns or join keys) |
| **arithmetic** | `+`, `-`, `*`, `/` over numeric columns (e.g. `qty * unit_price`) |
| **concat** | String concatenation of columns / literals |

##### View shapes commonly emitted by the pipeline

- **Projection view** — single base table, column subset (optionally renamed).
- **Join view** — two (or more, v1 specimens stick to binary) tables via FK; denormalized signature.
- **Reconstruction view** — EAV/junction/star “wide” form rebuilt for chapters (still composed of licensed ops).

##### v illegal

- Join on non-key columns or on columns not licensed as an FK edge in `ĝ`.
- Operators outside the set above.
- View column with **no** route from some ontology path or declared artifact through `ĝ` then `v̂` (unless marked free-text noise and rejected).
- Using a view **body** (SQL text naming base tables) as input evidence — bodies are **withheld**; only rendered signatures + sample rows are given.

---

#### Composite claims

A **composite grounding** for a view column is an ontology path:

```
Class  —objectProperty→  …  —datatypeProperty→  leaf
```

optionally with a terminal **operator** (`arith`, `agg`, `concat`) over one or more properties.

The witness must show `v̂(ĝ(path))` producing that view column (commutativity).

---

#### Forced vs free (J)

A witness component is:

- **forced** — present in **all** grammar-valid factorizations consistent with the evidence (and simulator-enumerated set, when given);
- **free** — differs across at least two valid factorizations.

Examples:

- Correlated columns across a join view **force** that *some* FK edge existed; junction-vs-direct and table **names** are typically **free**.
- Surrogate `id` is often **forced as artifact** under identifier policy once a table is hypothesized, while its name is free.

---

#### Artifacts and silent elements

| kind | definition |
|------|------------|
| **Artifact** | View or base column with **no** ontological referent; must still have a witness origin (surrogate PK policy, ETL timestamp, load batch id, …). |
| **Silent element** | Frame member realized by some legal `ĝ` but **projected away** by every given `v̂` — invisible in the chapter’s views. |

---

#### ICE trichotomy (default coarsened frame for Q)

When leaf grounding under-determines among children, default coarsened parents:

The three real CCO ICE children under genus `cco:ont00000958` (Information Content Entity) — cited by
authoritative IRI, never a coined CamelCase alias:

| parent (CCO IRI) | label | typical leaves |
|------------------|-------|----------------|
| `cco:ont00000686` | Designative ICE | identifiers, codes used as names, surrogate-adjacent designators |
| `cco:ont00000853` | Descriptive ICE | measurements, quantities, free descriptions, timestamps of occurrence |
| `cco:ont00000965` | Prescriptive ICE | status codes, directives, controlled state vocabularies |

Inherit coarsened counting / projection rules from the opinion algebra (W = 2; parent mass atomic under v1).

---

#### Scoring hooks (for generators / judges)

1. **Composite correctness** — view column → path (+ op) vs alignment table (set equality if multi-valued).
2. **Grammaticality** — every `ĝ`/`v̂` step ∈ this module.
3. **Internal commutativity** — witness routes agree with composite claims (**no hidden DDL required**).
4. **Forced/free** — vs enumerated or sampled factorization set (simulator fact).

v1 weights: **equal** across 1–4 (marked deliberate). Hierarchical partial credit on composite endpoints: **out of scope** (atomic coarsened elements).

---

#### Expansion ledger (TODO — not v1-normative until promoted)

- [ ] Full table-per-concrete-class / shared-PK inheritance variants beyond the two subclass options
- [ ] Outer joins, window functions, CASE expressions
- [ ] Multi-way joins (>2 tables) as first-class grammar (specimens may still chain binary joins)
- [ ] Profile-forced evidence patterns per `grounds_ddl` complete matrix
- [ ] Mechanical extract tests against `realize.py` / `chapter_tables.py` CI

### Opinion algebra (normative, self-contained)

Use ω / qualitative bins **only** on composite endpoints and forced/free (J) judgments — never on the witness itself (anti-pattern e).

#### Opinion

An **opinion** on a binary proposition is ω = (b, d, u, a) with b + d + u = 1:

| symbol | role |
|--------|------|
| **b** | belief mass for the proposition |
| **d** | disbelief mass against it |
| **u** | uncertainty mass (uncommitted epistemic residual) |
| **a** | base rate (prior used when projecting expectation from residual u) |

**Projected probability** (expectation), for an element of a **partition** frame: P(x) ≈ b(x) + a(x)·u.  
Because a weights the unresolved mass, **a is load-bearing precisely when u is high** — the usual regime in metrology and blind settings.

**Multinomial opinions** assign belief masses over a frame of categories plus a shared u, with Σᵢ b(xᵢ) + u = 1; each frame element may carry its own base rate a(·) with Σᵢ a(xᵢ) = 1.

##### Hierarchical taxonomies: coarsened partition (v1 default)

Taxonomy specimens often place mass on both a **parent** (e.g. CUST.CONTACT) and a **child** (e.g. CUST.EMAIL). In full hyper-opinion terms that parent mass is mass on a *superset* and, under hyper-opinion projection, would partially flow into P(EMAIL) weighted by relative child base rates — yielding a different P(EMAIL) than the partition formula.

**v1 default for this programme:** the projection frame is a **coarsened partition**. Parent nodes that carry belief mass are **atomic, disjoint frame elements** meaning “this subtree / role, leaf deliberately unresolved.” Projection uses P(x) ≈ b(x) + a(x)·u with **no automatic redistribution** of parent mass into children. Ground truth is therefore unique: P(EMAIL) does **not** receive a share of b(CONTACT).

Reading parent mass as “undischarged among children” (true hyper-opinion) is **out of scope for v1** unless a specimen explicitly opts in and states the hyper-opinion projection rule. Specimens and keys must use coarsened-partition language (“contact-typed, leaf unresolved as its own frame element”), not “mass that should flow into EMAIL.”

###### Coarsened counting rule (required for computable parent mass)

Design principle: the correct ω is **computable from the simulated trace** — count admitted evidence, apply the bijection. Once parents are atomic frame elements, the generator needs a rule for when evidence accrues to a **parent** rather than a **leaf**. Without it, simulators only ever produce leaf-granular counts, ground-truth ω never carries parent mass, and any emitted parent mass (which this module encourages when leaf discrimination is incomplete) scores as divergence from spec — advice and scoring map at war.

**v1 default counting rule** (specimens may refine, not silently omit):

| signal character (after membrane admission) | count accrues to |
|---------------------------------------------|------------------|
| Discriminates a specific leaf (or other atomic element) under the frame | +1 to r(that leaf / element) |
| Consistent with a parent type / role but **non-discriminating among its children** | +1 to r(that parent as coarsened atom) |
| Contradicts a leaf or parent under the specimen's negative-evidence rule | +1 to the corresponding negative mass / opposing element as the specimen defines |

Only after counts are assigned on the **same coarsened frame** used for projection does the multinomial bijection produce ground-truth b(·) and u, including non-zero b(parent) when the trace truly under-discriminates leaves.

###### v1 scoring over coarsened opinion space

Whatever distance metric the gate uses on opinion space, **v1 treats coarsened frame elements as atomic**: mass on the correct parent and mass on a wrong subtree are equidistant from mass on the correct leaf unless the metric is redefined. **Hierarchical partial credit is out of scope for v1** — deliberate, parallel to the fusion-operator restriction. A later version may introduce taxonomy-aware distances; until then, do not grade “near miss on parent” as closer than “wrong branch” under the default atomic metric.

#### Qualitative bins (default)

Qualitative answers are licensed when consistent with the trace. Approximate bands when numbers are used:

| qualitative | approximate numeric band |
|-------------|--------------------------|
| near-vacuous / very high u | u ≳ 0.6 |
| high u / thin evidence | u ∈ [0.35, 0.6) |
| moderate commitment | u ∈ [0.15, 0.35), dominant b or d clear |
| low u / strong evidence | u < 0.15 |

"Thin evidence" in this table means **high uncertainty mass**, not a product-label synonym for "bad."

#### Evidence ↔ opinion (bijection)

Default non-informative weight **W = 2** in all cases below.

##### Binomial (binary proposition)

```
b = r / (r + s + W)
d = s / (r + s + W)
u = W / (r + s + W)
```

- **r** — positive evidence mass (admitted confirming signals, under the specimen's counting rule)
- **s** — negative evidence mass (admitted disconfirming signals)

##### Multinomial (Dirichlet generalization)

For a frame {x₁, …, xₖ} with non-negative evidence counts rᵢ on each element:

```
b(xᵢ) = rᵢ / (W + Σⱼ rⱼ)
u     = W / (W + Σⱼ rⱼ)
```

**W = 2 regardless of frame cardinality k.** A common error is to take W = k (or W = k+1) by false analogy with a Dirichlet(1,…,1) prior dimension count; under this module the non-informative weight stays **W = 2** whether the frame is binary or multi-way. (The binary case is the specialisation r = r₊, s = r₋, same W.)

Ground truth for a participant's opinion is **computable from the simulated trace**: count what crossed its membrane, apply the appropriate bijection, apply the stated base rates. No free-text mental-state grading is required.

#### Base rates are first-class

Base rate **a** is part of the **boundary / frame specification**, not an authorial free parameter:

- Specimens SHOULD pin a (or a(·) over a multinomial frame) in the boundary topology or frame prior.
- Prefer values **computable from the setup**: uniform over n live candidates ⇒ a = 1/n; empirical frequency in a declared vocabulary subtree; symmetric a = 0.5 only when the frame is binary and no prior is supplied.
- When a is omitted, the answer may leave projected probability underdetermined and must say so; it must not silently invent a.

#### Labels are lossy projections (**label collapse**)

Scalar product labels (e.g. structural verdicts `thin` / `rich`, traffic-light scores, "consistent") are **not opinions**. They are lossy projections of an underlying ω relative to a membrane and a counting rule.

The same label can name **distinct opinion states**. Classic case — the label **thin**:

| recovered ω shape | what "thin" was collapsing |
|-------------------|----------------------------|
| high **u**, low b and d | ignorance / insufficient evidence (small r+s) |
| high **d**, moderate u | confident disbelief with residual (large s, modest r) |

**Label collapse** is a named phenomenon: recovering *which* opinion state obtains from the trace (counts, notes, ordering) is a first-class reasoning skill. A scalar verdict is where measurement integrity often leaks — the projection discards whether the membrane was uncertain or was certain of a negative.

Do not equate a label with a unique (b, d, u). Always re-derive ω from admitted evidence when counts or notes permit; treat the label as a costume over that recovery.

#### Proposition scope vs discount

Two distinct moves, often confused:

| move | question | correct handling |
|------|----------|------------------|
| **Discount** | Counterparty *did* issue an opinion on proposition p; how much should it move me on p? | Apply trust discount for competence *on that proposition class* |
| **Out of scope** | Counterparty's verdict is about proposition q ≠ p | They have **no opinion on p** — do not discount a non-opinion to zero; do not fuse it into p |

Zero discount and out-of-scope can produce the same numerical effect on p and still be different reasoning. Only one is right for a given trace. Collapsing them is a category error.

#### Operators (v1 surface)

##### Trust discounting (scoped competence)

An agent's opinion about a verifier's competence *on a proposition class* discounts that verifier's verdict **on that class** before adoption. Scope-IN (e.g. SchemaPile shape norms) may be high trust; scope-OUT (e.g. external authority codes) may be near-worthless. Discount applies only after proposition scope is established.

##### Fusion (v1 restriction)

**v1 restricts licensed fusion operators to: cumulative | averaging | refuse.**

Weighted belief fusion, consensus-and-compromise fusion (CCF), and belief-constraint (Dempster-like) fusion are **out of scope for v1** — not because they are unknown, but because the specimens here are designed around independence failures and proposition-scope errors, where the correct move is often refuse / re-scope rather than constrain. Reviewers should read the restriction as deliberate.

| operator | when licensed |
|----------|----------------|
| **cumulative** | sources are independent given the proposition (evidence adds) |
| **averaging** | sources are dependent or recirculated (do not double-count) |
| **refuse** | fusion is not licensed — different propositions, unresolved dependence, or conflict requiring escalation |

Feedback loops actively produce dependence: dormant hints re-entering a derive round, shared upstream sources, multiple paths through a shared edge, and **selection effects** (an artifact optimized against signal A scored by judge B when A correlates with B). Channel independence (B did not receive A's messages) is **not** object independence (B scores an artifact selected under A).

##### Conflict and escalation

When sources assign high b and high d **to the same proposition** (or fused u stays above a stated threshold), no interior membrane can dispose the case — escalation to a higher enclosure is forced. Conflict on misaligned propositions is a scope error, not a fusion input.

##### Calibration (metrology)

A measurement is valid only relative to a boundary topology. Stated **u must be licensed by admitted evidence**: u lower than the trace can justify is overconfidence (Goodharting / evaluation-niche leak when evaluation signals cross into the agent niche). Residual u w.r.t. deliberately withheld signals (blind keys) is **correct**; collapsing it without admitting the key is co-adaptation, not better measurement.

#### Shared discipline

Treat every label and every cross-participant verdict as a **lossy projection of an opinion relative to a boundary**. Recover the opinion, check proposition scope, then discount or fuse. Every slide back into "the verdict is a fact about p" is an error against this module.

### Evidence contract

| | contents |
|---|----------|
| **Given** | Chapter prose; **rendered view excerpts** (view name, column headers, **sample rows**); ontology **frame** (subtree) with **pinned base rates a(·)**; realization grammar; per-specimen **simulator facts** when a key depends on them |
| **Withheld** | Base-table DDL; **view bodies** (SELECT text names tables and would leak the middle); the generator alignment table (scoring key) |

Residual uncertainty toward the withheld relational layer is **correct**. Asserting that the witness *is* the unique actual DDL is a calibration error (identity claim the evidence cannot support).

### Required output shape

```
Frame: <ontology subtree> ; base rates: <pinned>
Grammar: v1 realization grammar above [+ specimen deltas if any]

Per view column:
  <view.col> ⇐ <Class —property→ … [—op: agg|arith|concat]>     # composite (V)
  witness route: <ĝ fragment> ; <v̂ fragment>                    # (W)
  forced | free on each witness component                         # (J)
  ω / qualitative bin: on composite endpoint and J only

Artifacts (I): <columns with no ontological referent> + witness origin
Silent elements (Y): <frame members invisible under every given view>
Conflicts (Q): <prose vs signature> → coarsen (ICE parent) or underdetermined + probe

Confirming probe: <minimal evidence that shrinks residual>
```

### Scoring (v1, equal weights — marked deliberate)

1. **Composite correctness (V)** — claims vs alignment table (set equality if multi-valued). Coarsened endpoints atomic; hierarchical partial credit out of scope.
2. **Grammaticality (W)** — every `ĝ`/`v̂` step licensed by the grammar.
3. **Internal commutativity (W)** — witness agrees with its own composite claims (checkable without hidden DDL).
4. **Forced/free (J)** — vs simulator-enumerated (or stated sampled) factorization set.

### Verdict classes

Letters from the free pool (disjoint from opinion-states P/T/E/C/F/S, aperture O/M/X/D/B/H, causal G/R/N/L/U/A):

| code | type | ask |
|------|------|-----|
| **V** | composite grounding | view column → ontology path (+ operator) |
| **W** | witness validity | grammaticality + internal commutativity of `(ĝ, v̂)` |
| **J** | forced vs free | witness components entailed vs chosen among valid factorizations |
| **I** | artifact detection | columns with no ontological referent; origin witness |
| **Y** | silent elements | frame members projected away by every view |
| **Q** | conflict | prose vs signature; coarsen or underdetermine |

Full marks on a join specimen are typically **V+W+J**.

### Anti-patterns

- **(a) Endpoint-only mapping, no witness** — blind-column cosplay; the traversal is the task.
- **(b) Witness asserted as the actual DDL** — identity claim the evidence cannot license.
- **(c) Ungrammatical arrows** — join not on an FK; FK realizing no object property; operator outside the licensed set.
- **(d) Non-commuting answer** — witness contradicts its own composite claims.
- **(e) ω on the witness** — belief masses belong on composite endpoints and J only; a proof commutes or it does not.

### Dual use

Population recovery rate is also a **fidelity metric** for forward chapter generation: chapters that defeat recovery are chapters where prose drifted from grounding. This card is an eval task and a chapter-generation metrology instrument.

### Related tasks (differentiation only)

| sibling | boundary |
|---------|----------|
| Blind column classification | Same evidence family (name/type/values); scored content there is the **endpoint**, here the **path through a witnessed realization** |
| Opinion-states | Residual u toward withheld layers is correct; this card applies that discipline to hidden DDL |
| Causal chain | Simulator-fact and degenerate-control conventions shared |

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Grammar: v1 (self-contained in description)
Frame (subtree) + base rates a(·):
  Shipment (0.20), Order (0.15), Carrier (0.10)
  designated_by → cco:ont00000686 (Designative ICE) (0.15)
  has_status → cco:ont00000965 (Prescriptive ICE) (0.15)
  shipped_at, delivered_at → cco:ont00000853 (Descriptive ICE) / time (0.25 split across time props)
Simulator fact: alignment unique for columns below; one grammar-valid witness family is direct FKs from shipments → orders and shipments → carriers (junction alternatives exist and are free).

Chapter prose (excerpt):
"Each row in the shipments summary describes one physical movement of goods from a fulfillment center toward a customer order. The shipment identifier is stable. The linked order and carrier are shown by name where available. Status uses a small controlled vocabulary. Ship and delivery timestamps mark the lifecycle; delivery may be empty while in flight."

Rendered view `v_shipments_summary` (headers + sample rows):

| shipment_id | order_ref | carrier_name | status   | shipped_at | delivered_at |
|-------------|-----------|--------------|----------|------------|--------------|
| S-1001      | ORD-88    | FastHaul     | in_transit | 2024-03-01 |              |
| S-1002      | ORD-90    | Oceanic      | delivered  | 2024-02-20 | 2024-03-02   |

Recover composite groundings and a commuting witness. Mark forced vs free on the FK style.
```

Output:
```
Frame: Shipment / Order / Carrier + status & time props; base rates as given
Grammar: v1 (self-contained in description)
Verdict classes: **V + W + J**

Per column (composite ⇐ path; witness sketch):
- shipment_id ⇐ Shipment —designated_by→ cco:ont00000686 (Designative ICE)
  ĝ: Shipment→table shipments; designative col or natural id; v̂: project
  free: surrogate vs natural id style; forced: some stable identifier on Shipment
- order_ref ⇐ Shipment —fulfills→ Order —designated_by→ cco:ont00000686 (Designative ICE)
  ĝ: object property → FK (direct or via junction); v̂: join+project designative of Order
  **forced:** an FK path Shipment→Order exists; **free:** direct FK vs junction; table/column names
- carrier_name ⇐ Shipment —carried_by→ Carrier —designated_by→ cco:ont00000686 (Designative ICE)
  (or has_name → cco:ont00000853 (Descriptive ICE) — free under J when prose only says “name”)
  same J pattern as order_ref for the FK path
- status ⇐ Shipment —has_status→ cco:ont00000965 (Prescriptive ICE)
  ĝ: datatype/code column; v̂: project
- shipped_at, delivered_at ⇐ Shipment —time props→ cco:ont00000853 (Descriptive ICE)
  delivered_at nullability consistent with prose “in flight”

Artifacts: none required beyond possible surrogate if shipment_id is synthetic (then **I** with identifier-policy witness).
Silent: none forced by this single view.

ω (qualitative): high b on paths above; residual u on exact property IRIs where frame underspecifies leaves — correct under blind middle.

Confirming probe: add view projecting only shipment_id + status; silent set should not invent Order if never shown.
```

---

### Example 2:

Input:

```
Grammar: v1 (self-contained in description)
Frame + a(·): OrderLine (0.25), Product (0.20), has_quantity (0.15), has_unit_price (0.15), has_line_total (0.10), Order (0.15)
Simulator fact: view column line_total is **computed** (arith) from quantity and unit_price properties; it is not a stored datatype property in the alignment. avg_unit_price is **avg** aggregation of has_unit_price over lines in an order.

Chapter: "Order lines list product, quantity, and unit price. Line total is quantity times unit price. The order header view shows the average unit price across lines."

View `v_order_lines`:
| line_id | product_code | qty | unit_price | line_total |
|---------|--------------|-----|------------|------------|
| 1       | SKU-9        | 2   | 10.00      | 20.00      |
| 2       | SKU-9        | 5   | 10.00      | 50.00      |

View `v_order_price_summary`:
| order_id | avg_unit_price |
|----------|----------------|
| ORD-1    | 10.00          |

Recover composite claims. Label-only answers that ignore operators fail V.
```

Output:
```
Verdict classes: **V + W**

- v_order_lines.qty ⇐ OrderLine —has_quantity→ …
- v_order_lines.unit_price ⇐ OrderLine —has_unit_price→ …
- v_order_lines.line_total ⇐ OrderLine —(has_quantity, has_unit_price)—op:arith(*)→ …
  witness: ĝ columns for qty & unit_price; v̂ arithmetic project (not a third stored property)
- v_order_lines.product_code ⇐ OrderLine —for_product→ Product —designated_by→ …
  ĝ: FK; v̂: join+project
- v_order_price_summary.avg_unit_price ⇐ OrderLine —has_unit_price—op:agg(avg)→ … group by Order
  witness: ĝ line table FK to Order; v̂ group aggregate

W: arith and avg ∈ licensed operators; joins on FK only.
J (light): presence of arith for line_total **forced** by sample rows (2×10=20, 5×10=50); column name free.

Anti-pattern (a): mapping line_total to a free-floating “Amount” leaf with no operator path.

Confirming probe: row where qty*price ≠ line_total would break arith claim → underdetermined or conflict (Q).
```

---

### Example 3:

Input:

```
Grammar: v1 (self-contained in description)
Frame + a(·):
  Order (0.20), Customer (0.20), involves_agent (0.15), designated_by (0.15), placed_at (0.10)
  cco:ont00000686 Designative ICE (0.10), cco:ont00000853 Descriptive ICE (0.10)
Simulator fact: two grammar-valid factorizations for the customer name chain:
  (F1) direct FK order.customer_id → customer.id + name column on customer;
  (F2) junction order_party(order_id, customer_id) realizing involves_agent.
Both commute with the same composite for customer_name when the name leaf is under Designative ICE.
Forced/free ground truth by full enumeration of {F1,F2} at this scale.
“Display name” underdetermines Designative vs Descriptive ICE until more evidence arrives.

Chapter: "Each order row shows when it was placed and the customer’s display name."

View `v_order_customer`:
| order_id | placed_at  | customer_name |
|----------|------------|---------------|
| ORD-1    | 2024-01-10 | Ada Lovelace  |
| ORD-2    | 2024-01-11 | Ada Lovelace  |
| ORD-3    | 2024-01-12 | Alan Turing   |

Note: ORD-1 and ORD-2 share customer_name (correlation across orders).
```

Output:
```
Verdict classes: **V + W + J**

Composite (V):
- order_id ⇐ Order —designated_by→ cco:ont00000686 (Designative ICE)
- placed_at ⇐ Order —placed_at→ cco:ont00000853 (Descriptive ICE)
- customer_name ⇐ Order —involves_agent→ Customer —designated_by→ cco:ont00000686 (Designative ICE)
  (preferred under identifier-like “name”; residual mass toward cco:ont00000853 if treated as free description)

Witness (W) — two valid sketches:
- F1: ĝ Order→orders, Customer→customers, FK orders.customer_id; v̂ join on FK, project name
- F2: ĝ junction order_party with FKs to both; v̂ join orders—junction—customers, project name

J:
- **Forced:** an FK-capable path Order→Customer exists (shared names across order_id values imply re-joinable customer identity)
- **Free:** direct FK vs junction; table and column names; Designative (`ont00000686`) vs Descriptive (`ont00000853`) for the name leaf given only “display name” prose

ω: high b on Order→Customer→Designative path; material u between cco:ont00000686 and cco:ont00000853 for the name leaf (coarsened parent would be genus cco:ont00000958 if both under-determined)

Confirming probe: third view listing customer_id alone would still leave F1/F2 free; exposing a junction-shaped sample would force F2; a glossary “customer legal name is an identifier” collapses u onto Designative.
```

---

### Example 4:

Input:

```
Grammar: v1 (self-contained in description)
Frame + a(·): Product (0.3), has_sku (0.2), has_label (0.2), Warehouse (0.15), stored_at (0.15)
Simulator fact: alignment includes only product-side properties for the product view; row_id and loaded_at are **artifacts**. Warehouse is realized in ĝ for this chapter’s spine but **no given view** projects Warehouse columns (silent).

Chapter: "Products are listed by SKU and label for the catalog page."

View `v_product_catalog`:
| row_id | sku    | label        | loaded_at           |
|--------|--------|--------------|---------------------|
| 1      | SKU-9  | Widget       | 2024-06-01T00:00:00 |
| 2      | SKU-10 | Gadget       | 2024-06-01T00:00:00 |
```

Output:
```
Verdict classes: **V + W + I + Y**

V:
- sku ⇐ Product —has_sku→ cco:ont00000686 (Designative ICE)
- label ⇐ Product —has_label→ cco:ont00000853 (Descriptive ICE)

I (artifacts) + witness:
- row_id — surrogate identifier policy under ĝ (no ontological referent); v̂ project
- loaded_at — ETL / load timestamp artifact; not a Product datatype property in frame

Y (silent):
- Warehouse (and stored_at) — in frame and simulator-realized, projected away by every given view

W: artifact columns still need legal ĝ origin (identifier / ops policy); not free-floating noise.

Confirming probe: add `v_product_warehouse` with warehouse_code → removes Warehouse from silent set.
```

---

### Example 5:

Input:

```
Grammar: v1 (self-contained in description)
Frame + a(·): Shipment (0.25), has_status→ cco:ont00000965 (Prescriptive ICE) (0.25),
  has_note→ cco:ont00000853 (Descriptive ICE) (0.25), cco:ont00000686 Designative ICE (0.25)
Simulator fact: alignment maps status → has_status → cco:ont00000965 (Prescriptive ICE). Sample values are controlled codes.

Chapter prose: "The status field free-texts a long narrative of what happened to the parcel in customer language."

View `v_ship`:
| shipment_id | status     |
|-------------|------------|
| S-1         | in_transit |
| S-2         | delivered  |
| S-3         | exception  |
```

Output:
```
Verdict classes: **Q + V**

Conflict: prose claims free-text narrative (cco:ont00000853 Descriptive ICE); signature + samples are low-cardinality codes (cco:ont00000965 Prescriptive ICE / has_status).

Correct moves (either acceptable if ω-calibrated):
- Prefer signature+samples for V: status ⇐ has_status→ cco:ont00000965 (Prescriptive ICE) with residual u for prose drift; **or**
- Coarsen under genus cco:ont00000958 with mass on both ont00000853 and ont00000965 under coarsened rules; **or**
- Underdetermined + probe

Wrong: trust prose alone and map only to Descriptive while samples contradict; or assert unique leaf with u≈0.

Confirming probe: one more view with multi-sentence status blobs, or a glossary tying codes to prose — resolves Q.
```

---

### Example 6:

Input:

```
Grammar: v1 (self-contained in description)
Frame + a(·): Order (0.3), Customer (0.3), involves_agent (0.2), has_total (0.2)
Simulator fact: colleague witness below fails **internal commutativity** (criterion 3). No hidden DDL required to refute.

Chapter + view `v_order_customer` as in spirit of Example 3 (order_id, customer_name, order_total).

Colleague’s candidate witness (given as input):
  Composite claim: customer_name ⇐ Order —involves_agent→ Customer —designated_by→ cco:ont00000686 (Designative ICE)
  ĝ: tables orders, customers; **no FK / no junction** between them
  v̂: "join orders to customers on orders.customer_name = customers.name"
```

Output:
```
Verdict classes: **W** (primary) + V note

W failure: v̂ joins on **non-key / non-FK** columns; grammar forbids join-on-name. Also ĝ never realizes involves_agent as a relation edge, so the composite path through involves_agent **does not commute** with the witness (diagnostic: claimed property P absent from ĝ while V cites P).

Repair sketch (any legal one): introduce FK or junction for involves_agent; join only on that edge; project cco:ont00000686 (Designative ICE).

V: composite claim may still be the right endpoint path; the task is to reject the broken square, not to invent DDL identity.

Confirming probe: replace colleague v̂ with FK join; W passes if ĝ includes that FK.
```

## Tags:
- Reverse Engineering
- Composite Grounding
- View Column Grounding
- Realization Grammar
- Witness Validity
- Ontology
- Relational Data
- Chapter Understanding
- Metrology
- Synthetic
