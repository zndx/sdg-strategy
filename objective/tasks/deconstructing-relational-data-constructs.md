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
| **Z** | inter-layer relation | reinforce / conflict / drift / silent gap / artifact origin between named layers |

**Z subtypes** (required when Z is claimed):

| subtype | meaning |
|---------|---------|
| **reinforce** | two layers say the same thing with independent support |
| **conflict** | two layers disagree (cite both claims) |
| **drift** | prose or samples lag ontology/DDL (or vice versa) |
| **silent** | content in one layer has no counterpart in another where expected |
| **artifact** | relational/sample feature with no ontological referent (surrogate key, ETL stamp) — origin must be named |
| **role-tension** | rigid identity vs anti-rigid role / SCD denormalization vs formal roles |

Underdetermined: allowed when evidence cannot choose among Z subtypes or O leaves — state residual and a confirming probe (no letter burn).

### Required output shape

```
Package layers: R|S|P|O|Π present/absent/partial
Verdict classes: K | Z | K+Z | …

K inventory:
  <table/col> :
    R: …
    S: … | absent
    P: … | silent
    O: <IRI or path> | coarsened | absent
    Π: … | absent

Z relations:
  <layer_i> ⟂ <layer_j> : <subtype> — evidence: "…" vs "…"

Artifacts / silent ontology:
  …

Confirming probe: <minimal addition that resolves the largest residual>
```

### Scoring (v1, equal weight — marked deliberate)

1. **Inventory completeness (K)** — present layers listed; no invented layers; absences marked.
2. **Grounding accuracy** — O paths use real IRIs/frame members when O is given; no fake `cco:` tokens.
3. **Z correctness** — subtype matches evidence; conflicts cite both sides; reinforce requires independent support in each layer.
4. **Probe quality** — names a discriminating observation, not a restatement.

### Anti-patterns

- **(a) Essay without inventory** — narrative “deconstruction” with no K table.
- **(b) Ontology-only or DDL-only** — ignores other present layers.
- **(c) False reinforce** — claims layers agree when samples/prose/DDL diverge.
- **(d) Fake external IRIs** — CamelCase under `cco:`/`bfo:`; use opaque IRIs or `sdg:` coins.
- **(e) Silent conflict** — notices tension in prose but omits Z.

### Differentiation

| sibling | boundary |
|---------|----------|
| Composite grounding recovery | There: recover paths **from** views/prose with a witness. **Here:** layers are **given**; diagnose roles and tensions. |
| Blind column | Endpoint classification from column evidence alone; no multi-layer package. |
| Causal chain | Event causation in verify loops; not static construct layer maps. |

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Package layers present: R, S, P, O (Π absent).

R (DDL excerpt):
  CREATE TABLE shipments (
    shipment_id VARCHAR PRIMARY KEY,   -- surrogate-style business key
    order_id VARCHAR NOT NULL REFERENCES orders(order_id),
    carrier_id VARCHAR REFERENCES carriers(carrier_id),
    shipped_at TIMESTAMP NOT NULL,
    delivered_at TIMESTAMP,            -- nullable
    status VARCHAR NOT NULL
  );

S (samples):
  status ∈ {in_transit, delivered, exception}; delivered_at null iff status=in_transit in sample.

P (chapter):
  "Each row is one physical movement of goods. Status is a small controlled set.
   Delivery timestamp is filled only after successful handoff; may be empty in flight.
   order_id links to the originating customer order; carrier_id to the logistics partner."

O (frame pins):
  Shipment class; object properties to Order and Carrier;
  status → cco:ont00000965 (Directive ICE);
  shipped_at/delivered_at → cco:ont00000853 (Descriptive ICE);
  shipment_id → cco:ont00000686 (Designative ICE).

Deconstruct: K inventory for columns + Z relations that matter.
```

Output:
```
Package layers: R,S,P,O present; Π absent
Verdict classes: **K + Z**

K inventory (abbrev.):
- shipment_id: R=PK; S=stable ids; P=“stable identifier”; O=cco:ont00000686 (Designative ICE)
- order_id: R=FK→orders; P=originating order; O=object property to Order
- carrier_id: R=FK→carriers; P=logistics partner; O=object property to Carrier
- shipped_at / delivered_at: R=timestamps, delivered_at nullable; S=null pattern; P=in-flight rule; O=cco:ont00000853 (Descriptive ICE)
- status: R=VARCHAR NOT NULL; S=controlled codes; P=controlled set; O=cco:ont00000965 (Directive ICE)

Z:
- R ⟷ S ⟷ P on delivered_at nullability: **reinforce** (DDL null, sample pattern, prose “in flight”)
- R ⟷ O on status: **reinforce** (directive codes ↔ Directive ICE)
- Π: **silent** (absent) — no strategy pin in package

Confirming probe: row with status=delivered and delivered_at null would break the reinforce claim (Z→conflict).
```

---

### Example 2:

Input:

```
Package: R, S, P, O present.

R:
  customer_id PK;
  current_segment VARCHAR;          -- SCD-style current value
  risk_flag BOOLEAN;
  first_order_date DATE;
  -- single row per customer (type-1 style current snapshot)

S: risk_flag true on 12% of rows; segment changes over time are NOT historized in R.

P: "risk_flag is computed from recent returns and payment failures. Segment can change
   over the lifetime but customer_id is invariant. Analysts use the current snapshot for cohorts."

O:
  Customer as rigid continuant identity;
  HighRiskCustomer / segment labels as anti-rigid roles (enter/leave);
  no temporal role axioms in the given O excerpt.

Deconstruct with emphasis on role-tension between R and O; how P mediates.
```

Output:
```
Package layers: R,S,P,O present
Verdict classes: **K + Z**

K:
- customer_id: R=stable PK; P=invariant identity; O=rigid Customer — **aligns**
- current_segment, risk_flag: R=current denormalized attributes; S=point-in-time; P=admits change over lifetime + computed risk; O=anti-rigid roles

Z:
- R ⟷ O on segment/risk: **role-tension** — R stores current flags on the identity table; O treats high-risk/segment as roles that require enter/leave (or temporal) structure not present in R
- P ⟷ R: **reinforce** on “current snapshot” intent; P ⟷ O: **drift** risk if readers take flags as rigid types
- S: supports prevalence of risk_flag, not historization

Confirming probe: SCD-2 history table or role reification in R, or temporal role axioms in O — either reduces role-tension.

Anti-pattern (c): claiming full reinforce across R and O without noting anti-rigid vs current-flag mismatch.
```

---

### Example 3:

Input:

```
Package: R, S, P, O present.

R: shipments.status VARCHAR NOT NULL
S: status values {in_transit, delivered, exception} only
P: "The status field free-texts a long narrative of what happened to the parcel in customer language."
O: status → cco:ont00000965 (Directive ICE)  [simulator: alignment is directive codes]

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
- P ⟷ (R,S,O): **conflict** (and **drift** if P is outdated harness text)
  P asserts Descriptive-style narrative; S+O support Directive ICE codes
- R ⟷ S ⟷ O: **reinforce**

Residual: underdetermined whether to trust P or S+O without more evidence — default to S+O for operational semantics, keep u on P-drift.

Confirming probe: multi-sentence status blobs in S, or glossary mapping codes to prose narratives.
```

---

### Example 4:

Input:

```
Package: R, S, P, O present.

R:
  product_id VARCHAR PK,
  sku VARCHAR NOT NULL,
  label VARCHAR,
  row_id BIGINT,              -- extra
  loaded_at TIMESTAMP         -- extra

S: row_id sequential; loaded_at constant within load batch; sku unique.

P: "Products are listed by SKU and label for the catalog."

O: Product; sku → cco:ont00000686 (Designative ICE); label → cco:ont00000853 (Descriptive ICE).
   No properties for row_id or loaded_at in frame.

Deconstruct artifacts vs grounded columns.
```

Output:
```
Verdict classes: **K + Z**

K:
- sku, label: grounded columns (R+S+P+O align)
- row_id: R present; S technical; P silent; O absent
- loaded_at: R present; S batch-constant; P silent; O absent

Z:
- row_id, loaded_at: **artifact** — no O referent; origin = surrogate / ETL load policy in R
- P ⟷ O on sku/label: **reinforce**
- O ⟷ R on artifacts: **silent** (ontology does not mention them; legal as artifacts)

Confirming probe: if O gains an ETL run entity linking loaded_at, reclassify loaded_at from pure artifact to grounded.
```

---

### Example 5:

Input:

```
Package: R, S, P, O present. Π partial: strategy_id listed only.

R+S: orders table with customer_id FK; samples show valid RI.
P: chapter describes orders and customers by name.
O: includes Warehouse class and stored_at property in the frame excerpt,
   but no warehouse columns in R and no warehouse mention in P/S.

Simulator fact: warehouse is in the ontology frame for the release but not realized in this table package.

Deconstruct silence.
```

Output:
```
Verdict classes: **K + Z**

K: R,S,P cover Order/Customer; O frame also lists Warehouse/stored_at (**partial** relative to package tables).

Z:
- O ⟷ (R,P,S) on Warehouse: **silent** — ontology frame content has no relational or prose counterpart in this construct package
- customer path: **reinforce** across R,S,P (and O if Customer present)

Π: strategy_id present only — **partial**; cannot attribute silence to a specific lens/voices pin without more Π.

Confirming probe: warehouse table DDL or chapter section, or confirm O frame subset for this template excludes Warehouse (then K marks O.Warehouse as out-of-scope, not silent).
```

---

### Example 6:

Input:

```
Package: R, S, P, O present (same shipment package spirit as Example 1).

Colleague deconstruction (given):
  "All layers fully reinforce. status is free-text Descriptive ICE
   (cco:ont00000853). delivered_at nullability is unspecified in R."

Simulator fact: R has delivered_at NULL-allowed; S ties null to in_transit; O maps status to cco:ont00000965 (Directive ICE).

Critique the colleague output and supply a corrected K+Z.
```

Output:
```
Verdict classes: **K + Z** (correction)

Colleague failures:
- **(c) false reinforce** — ignores P/S/O vs any free-text claim on status
- **wrong O** — cco:ont00000853 for status contradicts simulator O (Directive ICE / cco:ont00000965)
- **false R claim** — delivered_at nullability is specified in R

Corrected K (status, delivered_at): as in Example 1 reinforce pattern for nullability; status → cco:ont00000965 (Directive ICE)

Z: colleague claim ⟷ package: **conflict** on status ICE branch; delivered_at: package **reinforce** across R,S,P

Confirming probe: none required to refute colleague — package already suffices (same spirit as composite-grounding non-commuting trap).
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

K: can inventory R roles (PK, measure, time, method code-like) only.
Z: **underdetermined** — no second layer to reinforce or conflict.

Confirming probe: add S (method code list vs free text) or O (amount → Descriptive ICE measure; method → Directive ICE vs Designative) to enable Z.

Anti-pattern (a): multi-page essay on “likely ontology” without marking O absent.
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
