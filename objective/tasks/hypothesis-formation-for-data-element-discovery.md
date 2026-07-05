# Hypothesis Formation for Data Element Discovery

## Description:
This task involves generating plausible, testable hypotheses to explain observed column values, table patterns, or discrepancies between data and the current ontology during the data element discovery and derivation process. Real-world data element elucidation typically spans several related tables. Reasoning must consider foreign key traversal to establish identity and context, as well as explicit decisions about which columns to include (e.g., promoting to direct properties or relationships) or exclude (e.g., to avoid redundancy or follow observed normalization patterns).

Hypotheses are formed in the presence of actual schema definitions (DDL) along with observed values, using large-scale mined schema corpora such as SchemaPile as the canonical structural reference for norms around keys, shapes, naming, and column co-occurrence.

A complete elucidation TERMINATES IN ONE OR MORE DATA ELEMENT RECORDS — the precise, registrable definition in the ISO/IEC 11179 sense, matching the shape of the vocabulary's ReferenceCategory annotations. A Data Element Record carries:

- **name** and one-sentence **definition** (genus + differentia)
- **concept binding** — object class + property, grounded in the ontology (BFO/CCO/sdg lineage); for *de novo* elements, the proposed registration (new class/property with grounding) stated as a checkable axiom skeleton
- **representation** — datatype, unit (with inference evidence), format/precision, and the value domain: enumerated permissible values or a described domain with constraints; sentinel tokens resolved to their true semantics (e.g. "N/A" = not-applicable to this object class vs "TBD" = value pending — these are NOT permissible values)
- **multiplicity/optionality** and any identity role (key participation)
- **evidence** — the specific columns, value statistics, FK traversals, and SchemaPile norms supporting the binding
- **confidence + falsification tests** — what observation would refute the hypothesis, and which verification instruments adjudicate (reasoner consistency/admission, structural metrology against SchemaPile norms, value-parse rates, congruence to the concept lens)

The task evaluates scientific thinking over structured relational data: proposing multiple explanations grounded in multi-table DDL structure, FK relationships, raw values, and the ontology vocabulary; DISCRIMINATING between them with tests; and — in the de novo case — detecting that the current vocabulary lacks the element and producing the registrable definition rather than forcing a bad fit.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
The following DDL was extracted for a cluster of related tables:

CREATE TABLE transactions (
    id BIGINT PRIMARY KEY,
    cust_ref VARCHAR(255) NOT NULL,
    order_id BIGINT NOT NULL,
    amount NUMERIC(18,2),
    created_at TIMESTAMP,
    status VARCHAR(50)
);

CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    placed_at TIMESTAMP
);

CREATE TABLE customers (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP
);

Observed values: 71% of transactions.cust_ref match customers.email exactly (case-insensitive); 26% are 12-char base36 tokens with no match in customers.id or email; 3% are empty strings. orders declares a customer_id FK; transactions declares none (order_id is an undeclared join). SchemaPile key norms: customer-referencing columns overwhelmingly use role_id naming (customer_id); customer dimensions co-locate surrogate id + email. The ontology defines Customer with hasIdentifier and hasEmailAddress data properties.

Form two hypotheses about the data element(s) represented by cust_ref. Each must terminate in Data Element Record(s), with FK-traversal and inclusion/exclusion decisions, and tests that discriminate between the hypotheses.
```

Output:
```
Hypothesis 1 — cust_ref is a single legacy element: a denormalized customer email reference predating the normalized dimension; the base36 tokens are a failed migration's surrogate leakage, and the empty strings are load defects.

Modeling: repair toward the norm — introduce transactions.customer_id (BIGINT, FK -> customers.id, SchemaPile role_id convention, matching orders); resolve via email match, then retire cust_ref. Exclude copying name/email into the fact table (dimension traversal, not duplication).

Data Element Record (H1):
- name: Customer Email Reference (legacy)
- definition: an email address identifying the transacting customer, recorded before customer normalization
- concept binding: object class Customer (sdg lineage, CCO-grounded agent); property hasEmailAddress
- representation: string, RFC-5321-shaped; value domain = syntactically valid email; "" is NOT permissible (load defect -> missing)
- multiplicity: exactly 1 per transaction (via the repaired FK); identity role: none (identifier is customers.id)
- evidence: 71% exact email overlap; orders.customer_id precedent; SchemaPile role_id dominance
- confidence: moderate. Falsification: if the 26% base36 population shows temporal clustering AFTER the email population (not before), the "legacy remnant" story inverts — see H2.

Hypothesis 2 — cust_ref multiplexes TWO data elements over one column: registered customers (email, resolvable) and guest checkouts (transient base36 session token, never registered). One column, two populations, two elements.

Modeling: split — nullable transactions.customer_id FK for the resolvable population; retain a guest_contact element for the token population; never promote guest tokens into customers (dimension pollution).

Data Element Records (H2):
- name: Customer Reference — definition: FK to the registered customer dimension; binding Customer/hasIdentifier; representation BIGINT surrogate; multiplicity 0..1; evidence: the 71% email-resolvable population.
- name: Guest Session Token — definition: opaque token identifying an unregistered transacting party; binding: a transient Party role (anti-rigid — a role, not a Customer subclass); representation: string, base36, length 12, value domain = pattern-constrained opaque; identity role: none; evidence: the 26% population with no dimension match.
- Discriminator rule: email-shaped -> Customer Reference; base36 -> Guest Session Token; "" -> missing.

Discriminating tests (run during derivation):
1. Temporal split: plot the two value populations over created_at. Legacy story (H1) predicts base36 BEFORE emails; guest story (H2) predicts interleaved forever. This single test separates the hypotheses.
2. Join test: base36 tokens against orders lacking customer_id — H2 predicts strong correlation (guest orders), H1 predicts none.
3. Structural: propose the H2 shape (nullable FK + guest attribute) and check against SchemaPile co-occurrence — transaction tables carrying both a customer FK and a contact/session column are a known minority pattern; measure its rate before accepting.
4. Membrane: the H2 role binding must admit through the reasoner (a Role that inheres in a Party, realized in the transaction) without making Customer and Guest disjoint-by-accident; reasoner rejection of the role axioms refutes the H2 binding, not the H2 populations.
```

---

### Example 2:

Input:

```
The following DDL was extracted for a cluster of related tables:

CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(255),
    category_id BIGINT,
    created_at TIMESTAMP
);

CREATE TABLE product_attributes (
    product_id BIGINT NOT NULL,
    attr_name VARCHAR(100) NOT NULL,
    attr_value TEXT,
    effective_from DATE,
    PRIMARY KEY (product_id, attr_name, effective_from),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE attribute_definitions (
    name VARCHAR(100) PRIMARY KEY,
    data_type VARCHAR(50),
    unit VARCHAR(50),
    is_core BOOLEAN
);

Observed values for attr_name='net_weight': 94% parse as positive decimals; attribute_definitions gives data_type='decimal', unit='kg'; 4% are "N/A" (all on products in category 'digital-download'); 2% are "TBD" (all with effective_from in the future). For attr_name='color': free text, 40 distinct values, 8 cover 95% of rows. SchemaPile shape norms: weight-like attributes appear as dedicated columns on product tables in the majority of product schemas; color-like attributes split between dedicated columns and EAV.

Elucidate the data elements hiding in this EAV structure. Terminate in Data Element Records, resolve the sentinel semantics, and decide promotion vs EAV retention per SchemaPile norms.
```

Output:
```
The EAV rows are not one data element — attr_value is a CARRIER column multiplexing many elements, one per attr_name, each with its own representation recoverable by joining attribute_definitions and parsing values.

Data Element Record 1:
- name: Product Net Weight
- definition: the mass of one salable unit of the product, excluding packaging
- concept binding: object class Product; property a measurement-family data property (mass quality of an artifact, IAO measurement-datum lineage)
- representation: decimal, unit kg (declared by attribute_definitions AND corroborated by value magnitudes), precision from observed values (2dp typical), value domain: > 0
- sentinel resolution: "N/A" on digital-download products is NOT a value — it is an APPLICABILITY constraint: Net Weight applies to tangible products only (propose the axiom: the property's domain is TangibleProduct, a subclass the category column already witnesses). "TBD" with future effective_from is a PENDING value — temporal validity semantics, not a permissible string.
- multiplicity: 0..1 per (product, effective date) — the PK reveals the element is BITEMPORALLY VERSIONED: effective_from is part of the element's identity, so the full element is "net weight as of date".
- promotion decision: PROMOTE to products.net_weight_kg (SchemaPile majority pattern for weight-like attributes; is_core=true corroborates) — with the versioning caveat: promotion flattens history, so promote the CURRENT value and retain the EAV rows as the history relation.
- falsification: if >1 unit appears across categories (values bimodal around x2.2 suggests lb/kg mixture), the single-unit representation is refuted — split by unit evidence before promoting.

Data Element Record 2:
- name: Product Color (marketed)
- definition: the manufacturer-declared color descriptor of the product
- concept binding: Product; a descriptor-family property
- representation: string; value domain: OPEN enumeration — 8 values cover 95% (candidate controlled vocabulary), tail is free text; recommend an enumerated Kind class for the head with an open extension point, not a closed oneOf (the tail refutes closure)
- multiplicity: 0..1 per product per effective date
- promotion decision: RETAIN in EAV (SchemaPile split pattern; no is_core flag; open domain fits EAV's flexibility)
- falsification: if the 8-value head grows/rotates seasonally, the controlled-vocabulary hypothesis weakens toward pure free text.

Cross-cutting test plan: (1) parse-rate per attr_name (a data element candidate needs a dominant parse type); (2) unit corroboration — magnitude distribution vs declared unit; (3) applicability clustering — sentinel "N/A" correlating with a category PROVES a domain restriction, scattered "N/A" is just missingness; (4) propose promoted/retained shapes and re-score against SchemaPile shape norms; (5) the applicability axiom (TangibleProduct domain) must admit through the reasoner without unsat — rejection means the category witness is wrong, not the element.
```

---

### Example 3:

Input:

```
A harvested manufacturing document yields this table cluster (values sampled from the accompanying prose and tables):

CREATE TABLE work_orders (
    work_order_id BIGINT PRIMARY KEY,
    part_number VARCHAR(64) NOT NULL,
    quantity INT,
    released_at TIMESTAMP
);

CREATE TABLE cure_log (
    cure_log_id BIGINT PRIMARY KEY,
    work_order_id BIGINT REFERENCES work_orders(work_order_id),
    cure_temp_c NUMERIC(5,1),
    cure_dwell_min INT,
    ramp_rate_c_min NUMERIC(4,2),
    operator_badge VARCHAR(16)
);

Sampled values: cure_temp_c in [121.0, 176.5], tight modes at 121.1 and 176.7; cure_dwell_min in [45, 240]; ramp_rate_c_min in [0.5, 3.0]. The concept lens (vocabulary classification) returns no concept above the belief floor for any of the three cure_* columns — nearest hits are generic "Temperature Measurement" and "Duration" with low margins. SchemaPile co-occurrence shows process-parameter triplets (setpoint, dwell, ramp) recurring in process-log tables across manufacturing schemas.

The vocabulary lacks these elements. Perform de novo elucidation: detect the gap, form the hypothesis, and produce the registrable Data Element Records plus the ontology registration that verification instruments could admit or refute.
```

Output:
```
Gap detection: three mutually co-occurring columns classify BELOW the belief floor with low relative margins — the lens has no separating concept here. Forcing "Temperature Measurement" would be a category error (that concept is a generic quality-measurement; these columns are jointly the PARAMETERS OF ONE PROCESS). The co-occurrence triplet + the FK to work_orders + the value modes (121C / 177C are standard autoclave epoxy cure schedules) identify the missing concept: a thermal cure cycle.

Hypothesis: cure_log rows record executions of a CureCycle process; the three cure_* columns are its parameter data elements; the modes indicate the cycles run against a small set of standard RECIPES (a latent enumerated element not present as a column).

Proposed registration (checkable skeleton, sdg lineage):

Class: sdg:CureCycle
    SubClassOf: bfo:0000015,            # process, via the CCO process bridge
        sdg:executesFor exactly 1 sdg:WorkOrder,
        sdg:cureTemperatureSetpoint some xsd:decimal,
        sdg:cureDwellDuration some xsd:integer,
        sdg:rampRate some xsd:decimal

Data Element Records:
1. name: Cure Temperature Setpoint — definition: the target cure temperature of one cure cycle execution. Binding: CureCycle / cureTemperatureSetpoint. Representation: decimal(5,1), unit degC (column suffix _c + magnitude corroboration), value domain 20.0-250.0 with modal recipes at 121 and 177. Multiplicity: exactly 1. Evidence: column, modes, autoclave-standard values.
2. name: Cure Dwell Duration — definition: time held at setpoint. Binding: CureCycle / cureDwellDuration. Representation: integer, unit minutes (suffix _min), value domain 1-1440, observed 45-240. Multiplicity: exactly 1.
3. name: Temperature Ramp Rate — definition: heating rate approaching setpoint. Binding: CureCycle / rampRate. Representation: decimal(4,2), unit degC/min (suffix _c_min), value domain 0.1-10.0. Multiplicity: exactly 1.
4. name: Cure Recipe (LATENT) — definition: the standard schedule a cycle instantiates. Binding: proposed Kind class enumerating observed (setpoint, dwell, ramp) clusters. Representation: enumerated; evidence: two dominant value-triplet clusters. Registration deferred pending cluster stability across more documents.

Verification plan (instruments adjudicate, not the proposer):
1. Reasoner admission: the skeleton must be consistent and introduce zero unsatisfiable classes against the BFO/CCO backbone (process grounding must not collide with continuant-only property domains).
2. Structural projection: the registered class must project to DDL reproducing the observed shape — one table, three parameter columns, FK to work_orders — and its key election must match the observed surrogate pattern; a projection that invents structure the evidence lacks refutes the modeling.
3. Norm conformity: snake_case, unit-suffixed parameter columns, process-log co-occurrence — all majority patterns in SchemaPile manufacturing schemas; deviation flags the proposal.
4. Lens closure: after registering the concepts and re-indexing, the SAME columns must classify above the belief floor with healthy margins — the gap must actually close, and neighboring concepts must not lose separation (no aperture damage).
5. Falsification: dwell values parsing as clock times (not durations) refutes element 2's representation; temperature bimodality at a x1.8 ratio would suggest degF/degC mixture refuting the single-unit domain; operator_badge correlating with parameter drift would indicate the elements are measurements (actuals) rather than setpoints — a DIFFERENT concept binding (measurement datum vs specification), which test 1's domain axioms would then have to re-admit under the corrected lineage.
```

## Tags:
- Hypothesis Formation
- Data Element Discovery
- Data Element Registration
- Value Domains
- ISO/IEC 11179
- De Novo Discovery
- Relational Data
- Ontology Alignment
- Critical Thinking
- Scientific Method
- Schema Analysis
- Foreign Key Traversal
- Synthetic

## Citations:
- ISO/IEC 11179-3 — Metadata registries: data element metamodel (concept + representation)
- sdg-strategy objective/README.md — programme constitution (de novo Data Element elucidation as the bespoke model's terminal capability)
