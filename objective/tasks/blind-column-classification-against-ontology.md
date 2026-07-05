# Blind Column Classification Against Ontology Vocabulary

## Description:
This task requires classifying relational columns (given only their name, data type hints, representative values, table context, and chapter prose) against a hierarchically structured ontology vocabulary. The vocabulary is provided with explicit parent-child relationships (using dot-notation codes and parent pointers).

Rather than emitting a single point label or softmax distribution, the required output is a **reasoned opinion** in the style of Subjective Logic. The reasoner must assign:

- Belief mass (b) to specific categories or to composite sets representing subtrees (capturing the hierarchical nature of the taxonomy).
- An explicit uncertainty mass (u) representing epistemic uncertainty remaining after considering the available evidence (small samples, ambiguous context, blind setting with no reference key).
- Implicit or stated base rates (a) for projection.

This framing captures the essence of the hierarchical probability distributions produced by models such as the hierarchical NHSVM (Crammer-Singer style) used in Atelier: the model produces a distribution over the taxonomy tree, but the Subjective Logic view cleanly separates committed belief from uncommitted uncertainty and supports principled hierarchical reasoning (e.g., mass on a parent node when the evidence supports the broader category but is insufficient to distinguish children).

The task mirrors the blind classification setting used by Atelier as an independent efficacy gate over sdg-corpora releases.

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

Classify the following column from a blind perspective. Produce a Subjective Logic-style opinion (belief masses on categories or subtrees + uncertainty mass) together with reasoning:

Table: orders
Column: cust_email
Type hint: varchar
Sample values: ["alice@example.com", "bob.smith@corp.co", "guest-9921@temp.mail"]
Table context from chapter: "The orders table records purchases. cust_email captures the contact address provided at checkout; for logged-in users this usually matches the customer master record."
```

Output:
```
Subjective Opinion (multinomial over the CUST subtree, in the spirit of Subjective Logic):

- b(CUST.EMAIL) = 0.68
- b(CUST.CONTACT) = 0.12     # mass on parent: evidence supports contact role but limited discrimination between email vs other channels
- b(CUST.NAME) = 0.05
- b(CUST.IDENTIFIER) = 0.02
- u = 0.13                    # uncommitted uncertainty (blind setting, small sample, possible dual use as identifier in guest flows)

Base rate (a) derived from vocabulary frequency in the broader CUST subtree: a(CUST.EMAIL) ≈ 0.35 (relatively common contact attribute).

Projected probability (b + u·a):
- CUST.EMAIL ≈ 0.68 + 0.13*0.35 ≈ 0.725
- CUST.CONTACT (as category) remains high when uncertainty is considered at the parent level.

Reasoning:
- Strong positive evidence for CUST.EMAIL: sample values are canonical email addresses; chapter language explicitly uses "contact address".
- Some belief mass is deliberately placed on the CUST.CONTACT parent rather than forcing a leaf decision. This reflects the hierarchical nature of the taxonomy and the fact that the evidence (while pointing to contact) does not strongly distinguish EMAIL from other future contact subtypes.
- Residual uncertainty mass (u=0.13) is warranted in the blind setting: without the withheld reference we cannot rule out that in this particular construct the column was intentionally modeled under CUST.IDENTIFIER (e.g., for guest users where email doubles as the key).
- An NHSVM-style hierarchical classifier would likely produce a probability distribution with high mass on CUST.EMAIL but non-negligible probability mass remaining in the CUST.CONTACT subtree. The Subjective Logic framing makes the epistemic component explicit rather than burying it inside a calibrated softmax.

This opinion can be used directly for downstream fusion (Dempster-Shafer or Subjective Logic combination operators) with other evidence sources or for pignistic decision making.
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

Classify the following column from a blind perspective. Output a Subjective Logic opinion reflecting hierarchical uncertainty:

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
- b(FIN.TXN.ATTRIBUTE) = 0.06     # small mass on generic parent reflecting possible mis-categorization in source
- b(FIN.TXN.IDENTIFIER) = 0.01
- u = 0.11

Base rate a(FIN.TXN.QUANTITY) ≈ 0.22 within the FIN.TXN frame.

Projected probability:
- FIN.TXN.QUANTITY ≈ 0.78 + 0.11*0.22 ≈ 0.804

Reasoning:
- Dominant belief in FIN.TXN.QUANTITY driven by integer distribution, small positive values, and explicit chapter statement that it is multiplied by unit_price to obtain a total.
- Very low belief in FIN.TXN.AMOUNT because the values lack monetary characteristics (no decimals, no currency variation visible in samples).
- Modest mass on the FIN.TXN.ATTRIBUTE parent acknowledges that in some source systems a "qty" column can be overloaded with auxiliary flags; the blind view cannot fully exclude this.
- The uncertainty mass (u = 0.11) is lower than in the previous example because the chapter language is direct and the data type + value pattern are highly diagnostic. An NHSVM hierarchical model would typically place the large majority of its probability mass on the QUANTITY leaf while still leaving a small tail on the parent FIN.TXN node and siblings.

This opinion cleanly separates the model's hierarchical preference (strong for QUANTITY) from residual epistemic uncertainty that would be useful when fusing with other classifiers or when deciding whether to escalate the column for human review in a blind gate.
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