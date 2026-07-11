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

### Normative modules

| module | role |
|--------|------|
| **Realization grammar** | Licensed `ĝ` / `v̂` forms, illegal arrows, forced/free definition, ICE coarsening for conflicts. Include by reference: [`_realization-grammar.md`](./_realization-grammar.md). |
| **Opinion algebra** | ω / qualitative bins, W = 2, coarsened partition, base-rate pinning. Authoring extract: [`_opinion-algebra.md`](./_opinion-algebra.md); full normative text also lives in the opinion-states and blind-column cards. Use ω **only** on composite endpoints and forced/free judgments — never on the witness itself. |

JSON task export **inlines** the realization grammar (and opinion algebra surface as needed) mechanically.

### Evidence contract

| | contents |
|---|----------|
| **Given** | Chapter prose; **rendered view excerpts** (view name, column headers, **sample rows**); ontology **frame** (subtree) with **pinned base rates a(·)**; realization grammar; per-specimen **simulator facts** when a key depends on them |
| **Withheld** | Base-table DDL; **view bodies** (SELECT text names tables and would leak the middle); the generator alignment table (scoring key) |

Residual uncertainty toward the withheld relational layer is **correct**. Asserting that the witness *is* the unique actual DDL is a calibration error (identity claim the evidence cannot support).

### Required output shape

```
Frame: <ontology subtree> ; base rates: <pinned>
Grammar: _realization-grammar.md [+ specimen deltas if any]

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
Grammar: _realization-grammar.md
Frame (subtree) + base rates a(·):
  Shipment (0.20), Order (0.15), Carrier (0.10)
  designated_by → DesignativeICE (0.15)
  has_status → PrescriptiveICE (0.15)
  shipped_at, delivered_at → DescriptiveICE / time (0.25 split across time props)
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
Grammar: _realization-grammar.md
Verdict classes: **V + W + J**

Per column (composite ⇐ path; witness sketch):
- shipment_id ⇐ Shipment —designated_by→ DesignativeICE
  ĝ: Shipment→table shipments; designative col or natural id; v̂: project
  free: surrogate vs natural id style; forced: some stable identifier on Shipment
- order_ref ⇐ Shipment —fulfills→ Order —designated_by→ DesignativeICE
  ĝ: object property → FK (direct or via junction); v̂: join+project designative of Order
  **forced:** an FK path Shipment→Order exists; **free:** direct FK vs junction; table/column names
- carrier_name ⇐ Shipment —carried_by→ Carrier —designated_by→ DesignativeICE (or has_name→DescriptiveICE)
  same J pattern as order_ref
- status ⇐ Shipment —has_status→ PrescriptiveICE
  ĝ: datatype/code column; v̂: project
- shipped_at, delivered_at ⇐ Shipment —time props→ DescriptiveICE
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
Grammar: _realization-grammar.md
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
Grammar: _realization-grammar.md
Frame + a(·): Order (0.2), Customer (0.2), involves_agent (0.15), designated_by (0.15), NameICE under Designative (0.15), placed_at (0.15)
Simulator fact: two grammar-valid factorizations for the customer name chain:
  (F1) direct FK order.customer_id → customer.id + name column on customer;
  (F2) junction order_party(order_id, customer_id) realizing involves_agent.
Both commute with the same composite for customer_name. Forced/free ground truth by full enumeration of {F1,F2} at this scale.

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
- order_id ⇐ Order —designated_by→ DesignativeICE
- placed_at ⇐ Order —placed_at→ DescriptiveICE
- customer_name ⇐ Order —involves_agent→ Customer —designated_by→ NameICE (Designative)

Witness (W) — two valid sketches:
- F1: ĝ Order→orders, Customer→customers, FK orders.customer_id; v̂ join on FK, project name
- F2: ĝ junction order_party with FKs to both; v̂ join orders—junction—customers, project name

J:
- **Forced:** an FK-capable path Order→Customer exists (shared names across order_id values imply re-joinable customer identity)
- **Free:** direct FK vs junction; table and column names; whether name is designative vs descriptive leaf under NameICE

ω: high b on composite path; u on leaf NameICE vs broader Designative when prose only says “display name”

Confirming probe: third view listing customer_id alone would still leave F1/F2 free; exposing a junction-shaped sample would force F2.
```

---

### Example 4:

Input:

```
Grammar: _realization-grammar.md
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
- sku ⇐ Product —has_sku→ DesignativeICE
- label ⇐ Product —has_label→ DescriptiveICE

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
Grammar: _realization-grammar.md
Frame + a(·): Shipment (0.25), has_status→PrescriptiveICE (0.25), has_note→DescriptiveICE (0.25), DesignativeICE (0.25)
Simulator fact: alignment maps status → has_status (PrescriptiveICE). Sample values are controlled codes.

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

Conflict: prose claims free-text narrative (DescriptiveICE); signature + samples are low-cardinality codes (PrescriptiveICE / has_status).

Correct moves (either acceptable if ω-calibrated):
- Prefer signature+samples for V: status ⇐ has_status→PrescriptiveICE with residual u for prose drift; **or**
- Coarsen to parent ICE undecided between Descriptive/Prescriptive with mass on both children under coarsened rules; **or**
- Underdetermined + probe

Wrong: trust prose alone and map to free-text Descriptive while samples contradict; or assert unique leaf with u≈0.

Confirming probe: one more view with multi-sentence status blobs, or a glossary tying codes to prose — resolves Q.
```

---

### Example 6:

Input:

```
Grammar: _realization-grammar.md
Frame + a(·): Order (0.3), Customer (0.3), involves_agent (0.2), has_total (0.2)
Simulator fact: colleague witness below fails **internal commutativity** (criterion 3). No hidden DDL required to refute.

Chapter + view `v_order_customer` as in spirit of Example 3 (order_id, customer_name, order_total).

Colleague’s candidate witness (given as input):
  Composite claim: customer_name ⇐ Order —involves_agent→ Customer —designated_by→ NameICE
  ĝ: tables orders, customers; **no FK / no junction** between them
  v̂: "join orders to customers on orders.customer_name = customers.name"
```

Output:
```
Verdict classes: **W** (primary) + V note

W failure: v̂ joins on **non-key / non-FK** columns; grammar forbids join-on-name. Also ĝ never realizes involves_agent as a relation edge, so the composite path through involves_agent **does not commute** with the witness (diagnostic: claimed property P absent from ĝ while V cites P).

Repair sketch (any legal one): introduce FK or junction for involves_agent; join only on that edge; project NameICE.

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
