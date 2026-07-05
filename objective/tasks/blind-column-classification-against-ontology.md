# Blind Column Classification Against Ontology Vocabulary

## Description:
This task requires classifying relational columns (given only their name, data type hints, representative values, table context, and chapter prose) into the appropriate concepts from a provided ontology-derived vocabulary, without access to any withheld reference mappings or ground-truth labels. It evaluates the model's ability to perform the same blind classification that an independent judge (such as Atelier) would perform, using only the visible signals that would be available in a real deployment of the sdg-corpora data product.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Vocabulary excerpt (codes and labels):
- CUST.IDENTIFIER: Customer identifier
- CUST.NAME: Legal or display name of a customer or organization
- TXN.AMOUNT: Monetary amount of a transaction or line item
- TXN.TIMESTAMP: Point in time when a transaction or event occurred
- REL.FOREIGN_KEY: Reference to another entity via foreign key relationship

Classify the following column from a blind perspective:
Table: orders
Column: cust_email
Type hint: varchar
Sample values: ["alice@example.com", "bob.smith@corp.co", "guest-9921@temp.mail"]
Table context from chapter: "The orders table records purchases. cust_email captures the contact address provided at checkout; for logged-in users this usually matches the customer master record."
```

Output:
```
Primary classification: CUST.NAME (or more specifically a contact-oriented subclass if available)

Reasoning:
- The values are clearly email addresses, which function as human-readable identifiers or contact points rather than opaque surrogate keys.
- The chapter explicitly calls it a "contact address provided at checkout", aligning with name/contact semantics rather than pure identifier semantics.
- While it could serve as an identifier in some systems, the presence of recognizable name-like content (local part before @) and the chapter language favor a name/contact category over a pure CUST.IDENTIFIER.
- It is not a monetary amount or timestamp.
- REL.FOREIGN_KEY is unlikely because the values do not look like internal keys from another table.

Confidence notes for blind setting: Moderate. The email format is strong evidence, but without the reference we cannot know whether the original construct author chose to model this strictly as an identifier or as a contact attribute.
```

---

### Example 2:

Input:

```
Vocabulary excerpt:
- FIN.TXN.AMOUNT: Monetary value in a financial transaction
- FIN.TXN.QUANTITY: Count or quantity of items in a transaction line
- PROD.IDENTIFIER: Unique identifier for a product or SKU
- EVENT.TIMESTAMP: Time at which an event or state change was recorded

Classify this column blindly:
Table: order_lines
Column: qty
Type hint: integer
Sample values: [1, 2, 5, 12, 1]
Chapter note: "qty represents the number of units purchased for the line item. Always positive. Used together with unit_price to compute line total."
```

Output:
```
Primary classification: FIN.TXN.QUANTITY

Reasoning:
- Values are small positive integers with no decimal component, inconsistent with monetary amounts.
- The chapter directly states it is "the number of units purchased" and is multiplied by unit_price, which is the classic quantity role in transaction lines.
- Not a product identifier (values repeat across different products and are too small).
- Not a timestamp.
- The combination with a price column to derive a total is a strong indicator of the quantity semantic.

Alternative considered: Could be mis-modeled as amount in some source systems, but the explicit chapter language and integer distribution rule this out in favor of quantity.
```

## Tags:
- Column Type Annotation
- Blind Classification
- Relational Data
- Ontology Vocabulary
- Critical Thinking
- Data Interpretation
- Synthetic