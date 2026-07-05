# Reverse Engineering Constructs from Natural Language Chapters

## Description:
This task requires reconstructing a plausible relational construct (table name, columns with key designations, foreign key relationships, and ontology grounding hints) solely from a natural language chapter description of a data artifact, without seeing the original DDL or data. It evaluates the model's ability to perform the inverse of chapter generation: extracting structured relational semantics from prose while respecting the style and level of detail typically produced by the prose harnesses.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
The following is an excerpt from a generated chapter describing a data artifact:

"Each row in the shipments table represents one physical movement of goods from a fulfillment center to a customer address. The shipment_id is the stable identifier for the movement. order_id links back to the originating customer order. carrier_id identifies which logistics partner handled the delivery. shipped_at records when the package left the warehouse; delivered_at is populated only after successful handoff and may be null for in-flight shipments. The status column uses a small controlled set of values reflecting the current state of the movement."

Reverse engineer the most likely relational construct, including key designations and likely FK relationships.
```

Output:
```
Reconstructed construct:

Table: shipments

Columns:
- shipment_id (PK, surrogate or natural key for the movement)
- order_id (FK → orders.order_id)
- carrier_id (FK → carriers.carrier_id)
- shipped_at (timestamp, NOT NULL)
- delivered_at (timestamp, nullable)
- status (varchar or enum-like, controlled vocabulary)

Key structure:
- Primary key: shipment_id
- Foreign keys: order_id (to orders), carrier_id (to carriers)

Additional notes from prose:
- One-to-one or one-to-many relationship with orders (a single order may produce multiple shipments).
- delivered_at acts as a completion signal; its nullability is semantically meaningful.
- status is expected to be low-cardinality and aligned with an ontology-controlled list of shipment states.

This reconstruction would be validated by checking against the actual DDL spine in sdg-corpora and the corresponding ontology individuals for transportation events.
```

---

### Example 2:

Input:

```
Chapter excerpt:

"The product_attributes table is a flexible store for key-value style attributes that have not yet been promoted to dedicated columns. Each row ties a product (via product_id) to an attribute name and its value at a point in time. The attr_name column uses a controlled set of strings defined in the current vocabulary. Value can be text, numeric, or boolean depending on the attribute. effective_from provides temporal versioning for attributes that change over the product lifecycle."

Reverse engineer the construct.
```

Output:
```
Reconstructed construct:

Table: product_attributes (or product_attribute_values)

Columns:
- product_id (FK → products.product_id, part of key)
- attr_name (varchar, controlled vocabulary / reference to vocabulary)
- attr_value (varchar or variant; stores text, numbers as strings, or booleans)
- effective_from (timestamp or date, part of key for versioning)
- (possible) effective_to or is_current flag for SCD type 2 behavior

Key structure:
- Composite key likely on (product_id, attr_name, effective_from)
- Foreign key on product_id

Characteristics:
- Classic EAV (entity-attribute-value) pattern with temporal dimension.
- attr_name is expected to be governed by the ontology vocabulary rather than free text.
- The design trades normalization for flexibility; many attributes will later be promoted into the main products table or dedicated satellite tables during ontology maturation.

This structure is common in early corpus stages before full attribute promotion during realize and build_constructs steps.
```

## Tags:
- Reverse Engineering
- Relational Data
- Chapter Understanding
- Construct Design
- Analytical Thinking
- Pattern Recognition
- Synthetic