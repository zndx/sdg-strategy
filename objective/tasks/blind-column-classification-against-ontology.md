# Blind Column Classification Against Ontology Vocabulary

## Description:
This task requires classifying relational columns (given only their name, data type hints, representative values, table context, and chapter prose) against a hierarchically structured ontology vocabulary. The vocabulary is provided with explicit parent-child relationships (using dot-notation codes and parent pointers).

The required output is a **reasoned opinion** (belief masses, uncertainty, base rates) — a single leaf code without uncertainty is incomplete.

The reasoner **produces** an opinion over domain categories from column-level evidence in a **blind** setting (reference key withheld). Residual uncertainty with respect to the withheld key is correct.

This framing matches hierarchical probability distributions from models such as the hierarchical NHSVM (Crammer-Singer style): mass may sit on a parent when evidence supports the broader category but not a unique child.



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

Treat every label and every cross-participant verdict as a **lossy projection of an opinion relative to a boundary**. Recover the opinion, check proposition scope, then discount or fuse. Treating a verdict as a free-standing fact about p, without recovering ω and scope, is an error against this surface.
## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Hierarchical Vocabulary (code, label, parent_code):

- CUST: Customer or party concepts (root)
  - CUST.IDENTIFIER: Stable machine-oriented identifier for a customer or organization (parent: CUST)
  - CUST.NAME: Human-readable name or label (parent: CUST)
  - CUST.CONTACT: Contact or communication details (parent: CUST)
    - CUST.EMAIL: Electronic mail address used for contact or identification (parent: CUST.CONTACT)
    - CUST.PHONE: Telephone or messaging number (parent: CUST.CONTACT)

Frame prior (pinned base rates over the CUST subtree for projection):
- a(CUST.EMAIL) = 0.35
- a(CUST.CONTACT) = 0.20
- a(CUST.NAME) = 0.20
- a(CUST.IDENTIFIER) = 0.15
- a(other/unlisted under CUST) = 0.10

Classify the following column from a blind perspective. Produce a multinomial opinion (belief masses on categories or subtrees + uncertainty mass) using the pinned base rates for any projected probabilities.

Table: orders
Column: cust_email
Type hint: varchar
Sample values: ["alice@example.com", "bob.smith@corp.co", "guest-9921@temp.mail"]
Table context from chapter: "The orders table records purchases. cust_email captures the contact address provided at checkout; for logged-in users this usually matches the customer master record."
```

Output:
```
Subjective Opinion (multinomial over a **coarsened partition** of the CUST taxonomy):

Frame elements treated as disjoint for projection (v1 coarsened partition):
CUST.EMAIL | CUST.CONTACT | CUST.NAME | CUST.IDENTIFIER | (other mass absorbed in listed terms here)

- b(CUST.EMAIL) = 0.68
- b(CUST.CONTACT) = 0.12     # atomic coarsened element: contact-typed, leaf deliberately unresolved — NOT hyper-mass to redistribute into EMAIL/PHONE
- b(CUST.NAME) = 0.05
- b(CUST.IDENTIFIER) = 0.02
- u = 0.13
- Σb + u = 1.00

Base rates (from boundary/frame prior, not invented):
- a(CUST.EMAIL) = 0.35
- a(CUST.CONTACT) = 0.20
  (priors sum to 1 over the full pinned frame including NAME, IDENTIFIER, other)

Projected probability (partition formula only — parent mass does not flow into children):
- P(CUST.EMAIL) ≈ 0.68 + 0.13*0.35 ≈ 0.725
- P(CUST.CONTACT) ≈ 0.12 + 0.13*0.20 ≈ 0.146
  A hyper-opinion reading that folded b(CONTACT) into EMAIL via relative child base rates would yield a *different* P(EMAIL); that reading is out of scope for v1 and is not ground truth here.

Reasoning:
- Strong positive evidence for CUST.EMAIL: canonical email-shaped values; chapter says "contact address".
- Mass on CUST.CONTACT as its own coarsened outcome: evidence supports contact role while leaving open that the authoritative leaf might be CONTACT-general (or another channel) under the withheld key — committed belief in “contact-typed, leaf unresolved,” not uncommitted u and not a share of EMAIL.
- u = 0.13 licensed in the blind setting: dual-use as identifier in guest flows is not excluded (calibration: residual u w.r.t. key is correct).
- Emitting only the label CUST.EMAIL with no u would be **label collapse** — a lossy projection of this opinion.

Downstream: this ω is fusion-ready under the v1 operators above (cumulative only with independent sources; refuse double-counting).
```

---

### Example 2:

Input:

```
Hierarchical Vocabulary (code, label, parent_code):

- FIN.TXN: Financial transaction attributes (root)
  - FIN.TXN.AMOUNT: Monetary value (parent: FIN.TXN)
  - FIN.TXN.QUANTITY: Count or number of units (parent: FIN.TXN)
  - FIN.TXN.IDENTIFIER: Transaction or line identifier (parent: FIN.TXN)
  - FIN.TXN.ATTRIBUTE: Generic or auxiliary transaction attribute (parent: FIN.TXN)

Frame prior (pinned):
- a(FIN.TXN.AMOUNT) = 0.30
- a(FIN.TXN.QUANTITY) = 0.22
- a(FIN.TXN.IDENTIFIER) = 0.28
- a(FIN.TXN.ATTRIBUTE) = 0.20

Classify the following column. Output a Subjective Logic opinion reflecting hierarchical uncertainty.

Table: order_lines
Column: qty
Type hint: integer
Sample values: [1, 2, 5, 12, 1]
Chapter note: "qty represents the number of units purchased for the line item. Always positive. Used together with unit_price to compute line total."
```

Output:
```
Subjective Opinion (multinomial over the FIN.TXN subtree):

- b(FIN.TXN.QUANTITY) = 0.78
- b(FIN.TXN.AMOUNT) = 0.04
- b(FIN.TXN.ATTRIBUTE) = 0.06
- b(FIN.TXN.IDENTIFIER) = 0.01
- u = 0.11

Base rate a(FIN.TXN.QUANTITY) = 0.22 (pinned).

Projected probability:
- FIN.TXN.QUANTITY ≈ 0.78 + 0.11*0.22 ≈ 0.804

Reasoning:
- Dominant belief in QUANTITY: small positive integers; chapter multiplies by unit_price for line total.
- Low belief in AMOUNT: no monetary shape in samples.
- Modest mass on ATTRIBUTE: blind setting cannot fully exclude overloaded flags in other systems.
- u = 0.11 lower than Example 1: chapter language is direct and type+values are diagnostic — still non-zero because the reference key is withheld (licensed residual).

NHSVM-style hierarchical models would place most mass on QUANTITY with a tail on the parent/siblings; the opinion form makes the epistemic component explicit for fusion or escalation when fused uncertainty or conflict stays high.
```

## Tags:
- Column Type Annotation
- Blind Classification
- Hierarchical Classification
- Subjective Logic
- Uncertainty Quantification
- Evidential Reasoning
- NHSVM
- Relational Data
- Ontology Vocabulary
- Critical Thinking
- Data Interpretation
- Synthetic
