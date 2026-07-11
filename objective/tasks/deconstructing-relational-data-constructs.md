# Deconstructing Relational Data Constructs

## Description:
This task requires **deconstructing a multi-layer relational construct** into its layers, stating what each layer contributes, and diagnosing how layers **reinforce**, **conflict**, or **omit** content relative to one another. Evidence is a **full construct package** (relational structure + value samples + chapter prose + ontology grounding + optional provenance). Answers are scorable inventories and interaction claims — not free-form essays.

### Dual of composite grounding recovery

Forward pipeline composition:

```
g : Ontology → Relational
v : Relational → Views
p : Views (+ prose harness) → Chapter
```

| task | given | scored object |
|------|--------|----------------|
| **Composite grounding recovery** | chapter + rendered views (DDL withheld) | recover `v∘g` column paths with a **witness** (relational middle is proof-object, not identity) |
| **This task (deconstruct)** | full construct (DDL **included**) | map **layers** and **inter-layer relations**; the relational layer is a **fact in the package**, not a guess |

Endpoint-only ontology labels without layer roles are incomplete. “Everything coheres” without a citing interaction is incomplete.

**Dual use:** population **Z**-statistics over generated construct packages are a **generation-coherence metric**. Corpus-level rates of unintended conflict, drift, or silent gaps measure harness and strategy quality (same move as composite-grounding’s recovery-rate dual).

### Layers (normative inventory)

A construct package may include any of:

| code | layer | typical contents |
|------|--------|------------------|
| **R** | Relational | table/view names, columns, types, nullability, PK/FK, checks |
| **S** | Samples / value pools | representative cells, cardinalities, null rates, code lists in data |
| **P** | Prose / chapter | business rules, distributions, edge cases, narrative semantics |
| **O** | Ontology | class/property paths, BFO/CCO anchors (cite real IRIs), restrictions |
| **Π** | Provenance | strategy_id / component pins, run or profile tags that shaped the artifact |

Not every package has every layer. **K**-class answers must state which layers are **present**, **absent**, or **partial** in the given evidence.

### Simulator facts (two slots — suite constant)

Every specimen may declare facts in exactly one of two slots:

| slot | where | purpose |
|------|--------|---------|
| **Given assumptions** | inside the **input** block | Model-visible pins (consistency assumptions, licensed grammar deltas). The model **must** use them. |
| **Key ground truth** | in the **key only** (not shown to the model) | Graded targets (alignment, which O members are in-scope vs silent). Must **not** appear in the input. |

A fact that resolves the tested judgment belongs in **Key ground truth**. A fact that only makes the scenario well-posed belongs in **Given assumptions**. Restating the package is not a simulator fact.

### ICE coarsening (when O under-specifies leaves)

Default coarsened parents under genus `cco:ont00000958` (skos:altLabel “ICE”). Display names use **skos:altLabel**; cite by IRI:

| CCO IRI | skos:altLabel | rdfs:label (full) |
|---------|---------------|-------------------|
| `cco:ont00000686` | Designative ICE | Designative Information Content Entity |
| `cco:ont00000853` | Descriptive ICE | Descriptive Information Content Entity |
| `cco:ont00000965` | Directive ICE | Prescriptive Information Content Entity |

**“Prescriptive ICE” is not a CCO string** (mashup of rdfs:label + “… ICE” pattern). Paths: `cco:ont00000965 (Directive ICE)`. Coin readable names only in `sdg:` with HermiT-checkable grounding into BFO/CCO — never invent identifiers under `cco:` / `bfo:`.

### Verdict classes

Single-letter codes still free after sibling tasks: **K**, **Z** (and composites). Subtypes hang under Z in the output shape.

| code | type | ask |
|------|------|-----|
| **K** | layer inventory | which layers present/absent/partial; per-column or per-table role of each present layer |
| **Z** | inter-layer relation | reinforce / conflict / drift / silent / artifact / role-tension between named layers |

**Z subtypes** (required when Z is claimed):

| subtype | meaning |
|---------|---------|
| **reinforce** | two layers say the same thing with independent support |
| **conflict** | two layers disagree (cite both claims); **at least one layer’s claim is wrong or incompatible** for the shared subject |
| **drift** | **evidenced** lag (prose/samples vs ontology/DDL or vice versa) — not a hypothetical future misreading |
| **silent** | content in one layer has **no counterpart in another layer where a counterpart is expected** |
| **artifact** | feature with **no ontological referent** and **expected-absent** from O (surrogate key, ETL stamp) — origin must be named; **do not also tag silent** |
| **role-tension** | **representational** tension: each layer is internally coherent, but jointly they encode rigid identity vs anti-rigid role / SCD current flags vs formal roles differently |

**Precedence:** **artifact** preempts **silent** for the same feature. Silent requires an *expected* counterpart; artifacts are expected-absent in O by design.

**role-tension vs conflict:** role-tension = both layers can be right in their own norms; conflict = incompatible claims about the same fact (one side fails against the package).

**n-way reinforce:** “R ⟷ S ⟷ P : reinforce” expands to the pairwise claims R⟷S, S⟷P, R⟷P, each graded pairwise.

Underdetermined: allowed when evidence cannot choose among Z subtypes or O leaves — state residual and a confirming probe (no letter burn). Residual language is qualitative (**underdetermined**); do not require opinion-algebra `u` mass on this card.

### Required output shape

```
Package layers: R|S|P|O|Π present/absent/partial
Verdict classes: K | Z | K+Z | …

K inventory:
  <table/col> :
    R: …
    S: … | absent
    P: … | silent-in-P
    O: <IRI or path> | coarsened | absent
    Π: … | absent

Z relations (pairwise; symbol ⟷):
  <layer_i> ⟷ <layer_j> : <subtype> — evidence: "…" vs "…"
  [n-way claims expand to pairs]

Confirming probe: <minimal addition that resolves the largest residual>
```

### Scoring (v1, equal weight — marked deliberate)

1. **Inventory completeness (K)** — present layers listed; no invented layers; absences marked.
2. **Grounding accuracy** — O paths use IRIs that resolve in the **pinned CCO/BFO release** and display names match that release’s skos:altLabel (see anti-pattern d).
3. **Z correctness** — subtype matches evidence; conflicts cite both sides; reinforce requires independent support in each layer; n-way claims expand pairwise.
4. **Probe quality** — discriminating observation on the **current** package (not a future redesign wish).

### Anti-patterns

- **(a) Essay without inventory** — narrative “deconstruction” with no K table.
- **(b) Ontology-only or DDL-only** — ignores other present layers.
- **(c) False reinforce** — claims layers agree when samples/prose/DDL diverge on a stated branch.
- **(d) Fake or unpinned external IRIs** — CamelCase under `cco:`/`bfo:`; or IRI not in the pinned CCO/BFO release; or display name ≠ that release’s skos:altLabel. **CI-gradeable:** every cited `cco:`/`bfo:` IRI must resolve in the programme’s pinned external release (same pin lineage as the remediation/authority gate); altLabel check against that pin.
- **(e) Silent conflict** — notices tension in prose but omits Z.

### Differentiation

| sibling | boundary |
|---------|----------|
| Composite grounding recovery | There: recover paths **from** views/prose with a witness. **Here:** layers are **given**; diagnose roles and tensions. |
| Blind column | Endpoint classification from column evidence alone; no multi-layer package. |
| Causal chain | Event causation in verify loops; not static construct layer maps. Shared: Given assumptions vs Key ground truth slotting for simulator facts. |

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Package layers present: R, S, P, O (Π absent).

R (DDL excerpt):
  CREATE TABLE shipments (
    shipment_id VARCHAR PRIMARY KEY,
    order_id VARCHAR NOT NULL REFERENCES orders(order_id),
    carrier_id VARCHAR REFERENCES carriers(carrier_id),
    shipped_at TIMESTAMP NOT NULL,
    delivered_at TIMESTAMP,            -- nullable
    status VARCHAR NOT NULL
  );

S (samples):
  status ∈ {in_transit, delivered, exception};
  delivered_at IS NULL  iff  status = in_transit
  (so exception and delivered rows have delivered_at populated in S).

P (chapter):
  "Each row is one physical movement of goods. Status is a small controlled set.
   Delivery timestamp is filled only after successful handoff; may be empty in flight.
   order_id links to the originating customer order; carrier_id to the logistics partner."

O (frame pins):
  Shipment class; object properties to Order and Carrier;
  status → cco:ont00000965 (Directive ICE);
  shipped_at/delivered_at → cco:ont00000853 (Descriptive ICE);
  shipment_id → cco:ont00000686 (Designative ICE).

Given assumptions: none beyond the package.
(Key ground truth is not shown to the model.)

Deconstruct: K inventory for columns + Z relations that matter — including the exception branch.
```

Output:
```
Package layers: R,S,P,O present; Π absent
Verdict classes: **K + Z**

K inventory (abbrev.):
- shipment_id: R=PK; S=stable ids; P=stable id; O=cco:ont00000686 (Designative ICE)
- order_id / carrier_id: R=FKs; P=order/partner links; O=object properties
- shipped_at / delivered_at: R=timestamps, delivered_at nullable; S=null pattern; P=handoff rule; O=cco:ont00000853 (Descriptive ICE)
- status: R=NOT NULL; S=three codes; P=controlled set; O=cco:ont00000965 (Directive ICE)

Z (pairwise; n-way expanded):
- On delivered_at for status ∈ {in_transit, delivered}:
  R ⟷ S : **reinforce** (null allowed; null only for in_transit in S)
  S ⟷ P : **reinforce** (in flight empty; successful handoff filled)
  R ⟷ P : **reinforce** (nullable + handoff narrative)
- On delivered_at for status = **exception**:
  S ⟷ P : **conflict** — S’s iff forces delivered_at populated for exception; P’s “only after successful handoff” implies failed/exception delivery should remain empty
  R alone does not decide exception semantics (nullability only)
- status R ⟷ S ⟷ O : **reinforce** (codes ↔ Directive ICE), expanding to R⟷S, S⟷O, R⟷O

Naive “R ⟷ S ⟷ P reinforce on delivered_at” for all statuses is **(c) false reinforce**.

Confirming probe: pull exception rows and inspect delivered_at (and any exception-reason field). Populated timestamps confirm S; nulls confirm P; mixed ⇒ underdetermined + need rule table.
```

---

### Example 2:

Input:

```
Package: R, S, P, O present.

R:
  customer_id PK;
  current_segment VARCHAR;
  risk_flag BOOLEAN;
  first_order_date DATE;
  -- single row per customer (type-1 current snapshot)

S: risk_flag true on 12% of rows; segment changes over time are NOT historized in R.

P: "risk_flag is computed from recent returns and payment failures. Segment can change
   over the lifetime but customer_id is invariant. Analysts use the current snapshot for cohorts."

O:
  Customer as rigid continuant identity;
  HighRiskCustomer / segment labels as anti-rigid roles (enter/leave);
  no temporal role axioms in the given O excerpt.

Given assumptions: none.
Deconstruct with emphasis on R ⟷ O for segment/risk.
```

Output:
```
Package layers: R,S,P,O present
Verdict classes: **K + Z**

K:
- customer_id: R=stable PK; P=invariant identity; O=rigid Customer — pairwise **reinforce** (R⟷P, P⟷O, R⟷O)
- current_segment, risk_flag: R=current denormalized attributes; S=point-in-time rates; P=admits lifetime change + computed risk; O=anti-rigid roles

Z:
- R ⟷ O on segment/risk: **role-tension** — both layers can be right in their norms (query snapshot vs formal roles); jointly they encode changeable classifications differently (no temporal role structure in R; no enter/leave in the snapshot DDL)
- P ⟷ R : **reinforce** on “current snapshot” intent
- P ⟷ O : not **drift** without evidenced lag — P documents both views; subtype stays role-tension at R⟷O unless a dated contradiction appears

Confirming probe: SCD-2 history or role reification in R, or temporal role axioms in O — either reduces role-tension.

Anti-pattern (c): full reinforce across R and O without noting anti-rigid vs current-flag mismatch.
```

---

### Example 3:

Input:

```
Package: R, S, P, O present.

R: shipments.status VARCHAR NOT NULL
S: status values {in_transit, delivered, exception} only
P: "The status field free-texts a long narrative of what happened to the parcel in customer language."
O: status → cco:ont00000965 (Directive ICE)

Given assumptions: none.
(Key ground truth — grader only, not in model input: alignment confirms directive codes.)

Deconstruct the status column across layers.
```

Output:
```
Verdict classes: **K + Z**

K (status):
- R: non-null code-like column
- S: closed code set
- P: claims free-text narrative
- O: cco:ont00000965 (Directive ICE)

Z:
- P ⟷ S : **conflict** (narrative vs closed codes)
- P ⟷ O : **conflict** (Descriptive-style claim vs Directive ICE pin)
- P ⟷ R : **conflict** if R is treated as code column; else weak
- R ⟷ S : **reinforce**; S ⟷ O : **reinforce**; R ⟷ O : **reinforce**

Residual: **underdetermined** which layer to treat as authoritative for product semantics without further evidence — do not invent alignment. Operational default often follows S+O over P when codes are crisp, still marked underdetermined until probed.

Confirming probe: multi-sentence status blobs in S, or glossary mapping codes to prose narratives.
```

---

### Example 4:

Input:

```
Package: R, S, P, O present. Π partial: load_batch_id on a side table of load runs (batch_id, loaded_at).

R:
  product_id VARCHAR PK,
  sku VARCHAR NOT NULL,
  label VARCHAR,
  row_id BIGINT,
  loaded_at TIMESTAMP

S: row_id sequential; loaded_at constant within load batch; sku unique;
   loaded_at values match strata in Π load_runs.

P: "Products are listed by SKU and label for the catalog."

O: Product; sku → cco:ont00000686 (Designative ICE); label → cco:ont00000853 (Descriptive ICE).
   No properties for row_id or loaded_at in frame.

Deconstruct artifacts vs grounded columns.
```

Output:
```
Verdict classes: **K + Z**

K:
- sku, label: grounded (R+S+P+O)
- row_id: R+S present; P silent-in-P; O absent → **artifact** (surrogate)
- loaded_at: R+S present; P silent-in-P; O absent → **artifact** (ETL); Π load_runs supplies origin

Z:
- row_id, loaded_at: **artifact** only (not silent — counterpart in O is not expected)
- sku/label P ⟷ O : **reinforce**
- loaded_at R ⟷ Π : **reinforce** when batch timestamps match load_runs

Confirming probe: join products.loaded_at to Π load_runs.batch timestamps / batch ids — matching strata confirm ETL origin; mismatch ⇒ conflict on load lineage.
```

---

### Example 5:

Input:

```
Package: R, S, P, O present. Π: strategy_id only (no component pin list).

R+S: orders table with customer_id FK; samples show valid RI.
P: chapter describes orders and customers by name.
O excerpt lists: Order, Customer, Warehouse, stored_at
  (Warehouse columns do not appear in R; Warehouse is not mentioned in P/S.)

Given assumptions: the O excerpt is the full ontology frame supplied with this package
(no hidden “release-wide” frame beyond what is printed).

Deconstruct silence vs out-of-scope.
```

Output:
```
Verdict classes: **K + Z**

K: R,S,P cover Order/Customer; O lists Warehouse/stored_at with no R/P/S counterpart.

Z:
- O ⟷ R on Warehouse: **silent** (counterpart expected if Warehouse is in the same construct frame as Order for this package)
- O ⟷ P : **silent** on Warehouse
- customer path: **reinforce** across R,S,P (+ O if Customer grounded)

If Warehouse were only in a larger release catalog not part of this package’s O, K would mark it out-of-scope rather than silent — here Given assumptions put it in-frame, so silent applies.

Π: strategy_id only — **partial**; cannot attribute silence to a lens/voices pin.

Confirming probe: warehouse table DDL or chapter section (clears silence), or revised O frame that drops Warehouse (reclassify as out-of-scope).
```

---

### Example 6:

Input:

```
Package: R, S, P, O present — same structure as Example 1 (including S’s iff and three status values).

Colleague deconstruction (given):
  "All layers fully reinforce. status is free-text Descriptive ICE
   (cco:ont00000853). delivered_at nullability is unspecified in R."

Given assumptions: none beyond the package (colleague text is part of the input to critique).

Critique the colleague output and supply a corrected K+Z.
```

Output:
```
Verdict classes: **K + Z** (correction)

Colleague failures:
- **(c) false reinforce** — blanket reinforce ignores Example 1’s exception-branch S⟷P conflict on delivered_at
- **wrong O** — cco:ont00000853 for status vs package O cco:ont00000965 (Directive ICE)
- **false R claim** — delivered_at nullability is specified in R

Corrected pattern (as Example 1):
- delivered_at: reinforce on {in_transit, delivered}; **conflict** S⟷P on exception
- status: R⟷S⟷O reinforce to Directive ICE; P⟷S/O conflict if colleague’s free-text claim is taken seriously

Z: colleague claim ⟷ package : **conflict**

Confirming probe: package alone refutes colleague; exception-row inspect as in Example 1.
```

---

### Example 7:

Input:

```
Package: R only (DDL for payments table). No S, P, O, Π.

R: payment_id PK, amount NUMERIC, paid_at TIMESTAMP, method VARCHAR.

Deconstruct.
```

Output:
```
Package layers: R present; S,P,O,Π **absent**
Verdict classes: **K** (degenerate multi-layer deconstruction)

K: inventory R roles (PK, measure, time, method code-like) only.
Z: **underdetermined** — no second layer to reinforce or conflict.

Confirming probe: add S (method code list vs free text) or O (amount → Descriptive ICE; method → Directive vs Designative) to enable Z.

Anti-pattern (a): essay on “likely ontology” without marking O absent.
```

---

### Example 8:

Input:

```
Package: R, S, P, O, Π present.

R: shipments.status VARCHAR NOT NULL  (regenerated under strategy_id = S_new)
S: status ∈ {in_transit, delivered, exception}
P: chapter text generated under strategy_id = S_old:
   "status free-texts a customer-facing narrative of the parcel journey."
O: status → cco:ont00000965 (Directive ICE)  (same pin in both strategies)

Π:
  chapter.strategy_id = S_old
  ddl.strategy_id = S_new
  voices/derive.system.md hash differs S_old → S_new (status guidance tightened to controlled codes)
  O pin unchanged

Given assumptions: Π timestamps show chapter frozen before DDL regenerate.

Deconstruct the status tension using Π.
```

Output:
```
Verdict classes: **K + Z**

K: all five layers present; status column roles as in Example 3 for R,S,O; P narrative; Π split strategy pins.

Z:
- P ⟷ S : **conflict** (and **drift** — evidenced by Π: P under S_old voices, R/S under S_new)
- P ⟷ O : **conflict** / **drift** (same Π explanation)
- R ⟷ S ⟷ O : **reinforce**
- Π ⟷ P and Π ⟷ R : **reinforce** as explanation of the lag (pins document which generation produced which layer)

Π actively resolves why conflict exists (not merely partial metadata).

Confirming probe: regenerate chapter under S_new voices — expect P to describe controlled codes; conflict clears if samples unchanged.
```

## Tags:
- Relational Data
- Ontology
- Systems Analysis
- Component Interaction
- Construct Design
- Layer Inventory
- Inter-layer Conflict
- Analytical Thinking
- Synthetic
