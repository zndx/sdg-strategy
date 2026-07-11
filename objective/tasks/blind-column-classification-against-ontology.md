# Blind Column Classification Against Ontology Vocabulary

## Description:
This task requires classifying relational columns (given only their name, data type hints, representative values, table context, and chapter prose) against a hierarchically structured ontology vocabulary. The vocabulary is provided with explicit parent-child relationships (using dot-notation codes and parent pointers).

Rather than emitting a single point label or softmax distribution, the required output is a **reasoned opinion** under the shared subjective-opinion algebra.

**Normative opinion algebra** (ω, multinomial masses + u, base rates a(·), beta bijection with W = 2, qualitative bins, label collapse, calibration of u to admitted evidence, v1 fusion notes for downstream use): see [`_opinion-algebra.md`](./_opinion-algebra.md). That module is included by reference and is binding for this task.

First-order role of this task (vs second-order loop reasoning in *Boundary-Relative Opinion States in CAS Architectures*):

- Here the reasoner **produces** an opinion over domain categories from column-level evidence (blind: no reference key).
- There the reasoner **recovers** multi-participant opinions, scope, discount, and licensed fusion from message traces.

This framing matches hierarchical probability distributions from models such as the hierarchical NHSVM (Crammer-Singer style) in Atelier: mass may sit on a parent when evidence supports the broader category but not a unique child. Under the shared algebra's **v1 coarsened-partition default**, that parent mass is an atomic frame element (“subtree / role, leaf unresolved”) for projection — it does **not** hyper-redistribute into children. The opinion view separates committed belief from uncommitted uncertainty and keeps base rates explicit for projection (P(x) ≈ b(x) + a(x)·u; a is load-bearing when u is high).

**Base rates are first-class.** Specimens pin a(·) over the relevant vocabulary frame (empirical frequencies when given; otherwise state underdetermination). Do not silently invent a.

**Labels are lossy.** A single leaf code without u is a collapsed projection; the task requires the full opinion (masses + u + a), not a costume label alone.

The setting mirrors Atelier's blind classification gate over sdg-corpora releases: residual u w.r.t. the withheld reference is **correct**, not a defect.

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

Frame elements treated as disjoint for projection (v1 default — see _opinion-algebra.md):
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

Downstream: this ω is fusion-ready under the shared v1 operator rules (cumulative only with independent sources; refuse double-counting).
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

NHSVM-style hierarchical models would place most mass on QUANTITY with a tail on the parent/siblings; the opinion form makes the epistemic component explicit for fusion or escalation (high conflict / high fused u → human review under second-order loop rules).
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
