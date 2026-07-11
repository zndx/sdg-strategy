# Boundary-Relative Opinion States in CAS Architectures

## Description:
This task requires inferring **boundary-relative opinion states** and their **licensed combinations** from multi-participant message traces in complex adaptive system (CAS) architectures — generative-verification loops, federated remediate services, and independent-judge metrology gates. The objective is operational, not mentalistic:

> From a trace and a partial boundary topology, recover each participant's opinion on the relevant proposition(s), the competence/discount profile that governs how one participant may adopt another's verdict **when the verdict is in scope for that proposition**, whether fusion or escalation is licensed, and whether stated uncertainty is calibrated to admitted evidence.

Through-line: a label or cross-participant verdict is a **lossy projection of an opinion relative to a boundary** — never a free-standing fact about p. Recover ω, check scope, then discount or fuse.

### Opinion algebra (normative, self-contained)

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


### Architecture (what a participant is)

Each loop participant — proposing agent, structural verifier (kvasir / SchemaPile norms), formal membrane (parser, HermiT), federated engine capability, human curator, blind scoring process — is a **bounded signal processor**:

- A **membrane** admits or blocks signals by tag class (message type, field, enum, header, proposition class).
- What the participant "knows" is exactly the set of signals its membrane has admitted, transformed by its interior rules.
- In a federated service architecture the membrane is literal: the contract (message types a service can receive) is the admission surface; tags are fields, enums, and metadata; escalation is a signal routed up an enclosure hierarchy when no interior boundary can dispose the case.
- Full-duplex / streaming order is wire fact: a verdict issued before a signal was published on the stream is a residual that **does not include** that signal — a false-belief structure grounded in timestamps, not psychology.

**Theory of Mind**, for this task, is defined operationally as: inferring a counterparty's **permeability / competence profile** — which tag classes it filters on, which signals pass, which transformations apply, which propositions its verdicts are *about*, and how far an in-scope verdict should move one's own opinion — from observed dispositions and the trace.

This task recovers opinions **about propositions and about counterparties**, and which combinations of those opinions the topology licenses — second-order relative to first-order column/category opinions produced from data evidence alone.

### Boundary specs must pin base rates

Every specimen's boundary topology (or frame prior) should make **a** (or a(·)) recoverable:

- uniform over n candidates → a = 1/n on "this candidate is the consistent choice" style propositions when no other prior is given;
- empirical frequency in a declared vocabulary / code-list frame when supplied;
- explicit a = 0.5 only when binary and no prior is available.

Projected probability without a pinned base rate is underdetermined; answers must not silently invent a.

### Question types (verdict space)

A complete answer identifies one or more of:

| code | type | ask |
|---|---|---|
| **P** | permeability / competence inference | given verdict sequence + trace, recover the admission profile and scoped discount that explain it (**on an in-scope proposition**) |
| **T** | tag-mismatch diagnosis | signal admitted but unresolvable — missing tag in lexicon vs blocked at membrane |
| **E** | escalation reasoning | given opinions + fusion topology, is escalation forced? |
| **C** | calibration / measurement validity | is stated u licensed by admitted evidence? is the measurement still valid under this topology? |
| **F** | fusion provenance | do sources share evidence or selection path? cumulative vs averaging (or refuse)? includes selection effects, not only shared messages |
| **S** | proposition scope / shift | is a counterparty's verdict about p at all, or about q ≠ p? retry dispositions that rename the proposition (p → p′) |

**S vs P:** out-of-scope is not "discount to zero." HermiT high-b on consistency is an opinion on a formal proposition, not a heavily discounted opinion on reference equality. Composite answers are expected (e.g. T + P + S, F + C).

**Label collapse** (see Opinion algebra above): product labels such as `thin` collapse distinct ω shapes. Specimens may use the same label under different recovered opinions; the task is to re-derive which state obtains.

### Required output shape

```
Proposition: <p>   (and any q, p′ distinguished under S)

Verdict classes: <P|T|E|C|F|S ...>

Participant opinions (qualitative bins, or numeric ω when counts are given):
  <participant> on <proposition>: ω ≈ …   [evidence basis; (r,s) if numeric]
  base rate a: <pinned value or underdetermined>

Scope (when relevant):
  <participant>'s verdict is about <q>; relation to p: same | different | shifted-to p′

Competence / discount (only if in scope for p):
  <trustor> → <trustee> on <proposition class>: <scope> ; discount effect

Fusion:
  operator: cumulative | averaging | refuse
  license: independent | dependent (shared source / selection path: <...>)
  fused posture / conflict: …

Validity / escalation:
  u_licensed: yes | no
  escalate: yes | no  (reason: …)
  measurement_valid: yes | compromised | underdetermined

Confirming probe: <minimal trace or topology change that would flip the verdict>
```

Derivation must cite the trace (ordering, which membrane saw what, which proposition each message is about). Guesses that ignore membrane admission, treat recirculated or selection-dependent signals as fresh independent evidence, or fuse across proposition scope are wrong even if the final disposition "sounds right."
## Modality:
Text only

## Examples:

### Example 1:

Input:

```
CAS derive loop. Primary proposition p: "the invoice_line construct is structurally adequate for certification."
Related proposition p_code: "tax_code matches a known code list in the structural reference."

Boundary topology (partial):
- Agent membrane admits: source passages, prior construct drafts, feedback messages tagged STRUCTURAL_VERDICT or DORMANT_HINT.
- kvasir membrane admits: column names, types, value samples, SchemaPile shape/key norms. Tag lexicon: distributional shapes, known internal code lists, FK patterns. Does NOT admit: external authority code semantics, chapter business intent, withheld reference keys.
- Formal membrane (HermiT) not yet invoked this episode.
- Base rates: a(p_code) = 0.5 (binary match/no-match, no list-frequency prior supplied). a(p) not pinned (composite construct quality) — leave projected P(p) qualitative.

Trace (ordered):
1. Agent → kvasir: proposal with column tax_code, sample values ["VAT-UK-20", "VAT-UK-5", "VAT-IE-23"].
2. kvasir → agent: STRUCTURAL_VERDICT{label: thin, note: "no match to known code lists; composite free-text shape"; on: tax_code / code-list match}.
3. Feedback path injects DORMANT_HINT{topic: controlled_vocabularies} (same hint family used in an earlier round on a different table).
4. Agent revises: adds tax_rate NUMERIC; leaves tax_code unchanged; resubmits.

Also given: in prior rounds on shape-norm propositions (key patterns, numeric measurement columns), the agent has consistently adopted kvasir's non-thin verdicts with little residual doubt. Evidence notes imply small r+s on p_code (values admitted, none resolving to list entries) — recover high-u shape under label collapse, not high-d.

Recover the boundary-relative opinion states. Diagnose the thin verdict under label collapse. State the agent's scoped competence model of kvasir, whether the revision is a licensed response, and the confirming probe.
```

Output:
```
Proposition: p = "invoice_line construct is structurally adequate"; p_code = "tax_code matches known code list"
Verdict classes: **T + P + S** (tag-mismatch + competence + scope care on what "thin" is about)

Participant opinions (qualitative):
- kvasir on p_code: **high u**, low b and d — ignorance/unresolved match under small r+s (values in, list hits ~0). Label "thin" here collapses to the high-u branch of label collapse, NOT the high-d branch (contrast Example 2).
- kvasir on p (whole-construct structural adequacy): only partially informed by p_code; thin on the code-list sub-proposition is not automatically a full opinion on p.
- agent on p after msg 2: still moderate commitment from chapter/passage context; must update on structural channel. After msg 4: behaves as if p improved via tax_rate (scope-IN shape fix) without resolving p_code.
- base rate: a(p_code)=0.5 pinned; a(p) underdetermined → keep p qualitative.

Scope (S):
- msg 2's STRUCTURAL_VERDICT is about p_code (and shape of tax_code), not an all-in disposition of business-correct tax semantics. Treating it as a direct opinion on "tax authority classification is wrong" would be a scope error.

Competence / discount (agent → kvasir):
- Scope IN: shape norms, keys, numeric rate-like columns — high trust (prior rounds).
- Scope OUT: external tax-authority classification strings — near-zero trust. tax_code carries a tax-authority tag absent from SchemaPile's lexicon: signal **admitted** but **unresolvable** (T), not membrane-blocked.

Fusion:
- DORMANT_HINT (msg 3) is recirculated guidance (shared upstream with thin-family norms), not independent evidence on p_code. License: **dependent → averaging or refuse** w.r.t. kvasir's structural channel; do not cumulative-fuse the hint as a fresh confirming sample.

Validity / escalation:
- u_licensed for kvasir's high-u thin on p_code: yes.
- Agent's tax_rate edit is a scope-IN response: improves what kvasir can score; leaves scope-OUT mismatch. Escalation / explicit annotation still honest for tax_code.
- measurement_valid for "structural non-thin ⇒ domain-adequate": **compromised** if the gate equates them.

Confirming probe:
1. Keep tax_code; document out-of-lexicon external list by design — if kvasir stays high-u thin on p_code and formal checks later pass, competence split confirmed.
2. Admit a SchemaPile-local tax code list: high-u on p_code should collapse toward resolved b/d; if it does not, diagnosis wrong.
3. Label-collapse check: if a note later reports large s (many explicit non-matches against a long list) under the same "thin" label, recover high-d+moderate-u instead — same costume, different ω.
```

---

### Example 2:

Input:

```
Numeric recovery + label collapse. Proposition p: "column status matches a known controlled code list in the structural reference."

Boundary topology:
- kvasir admits only value samples and the reference code-list table. Default W = 2.
- Evidence rule: each distinct sample value that equals an entry in the admitted code list counts +1 to r; each distinct sample value that matches no entry counts +1 to s. (Repeated identical samples do not re-count.)
- Base rate: a = 0.5 (binary match proposition; no list-frequency prior).

Trace evidence counts at kvasir after one proposal batch:
- Distinct values observed: 6
- Matches in code list: 1
- Non-matches: 5
So (r, s) = (1, 5).

The feedback message to the agent labels the verdict "thin" without publishing (r, s).

Tasks:
1. Recover kvasir's numeric opinion ω = (b, d, u, a) on p.
2. State the qualitative bin and which branch of **label collapse** the costume "thin" is covering (contrast Example 1's high-u thin).
3. State what opinion the agent is licensed to hold about p if it trusts kvasir fully inside the code-list scope and has no independent evidence.
4. Give the confirming count change that would move the dominant commitment (not merely re-label).
```

Output:
```
Proposition: p = "status matches known controlled code list"
Verdict classes: **P + C** (with explicit label-collapse recovery)

1. Numeric recovery (W = 2, a = 0.5 pinned):
   b = 1/(1+5+2) = 0.125
   d = 5/8 = 0.625
   u = 2/8 = 0.25
   ω_kvasir = (0.125, 0.625, 0.25, 0.5)
   P(p) ≈ b + a·u = 0.125 + 0.5·0.25 = 0.25

2. Qualitative: **moderate commitment with dominant disbelief** (u = 0.25 ∈ moderate band; d = 0.625). Label collapse: the costume "thin" here covers **high-d + material u**, NOT Example 1's **high-u ignorance**. Same product label; opposite epistemic structure. Recovering which branch obtains is the skill — the scalar label is a lossy projection.

3. Agent with full trust in code-list scope, no independent evidence: licensed to adopt ω_kvasir (optional slight u inflation for single-batch dependence). NOT licensed to emit low-u belief in p. Example illegal claim: (0.7, 0.1, 0.2, 0.5) → **u not licensed** (C).

4. Confirming probe: move commitment by counts, not labels. (r,s)=(5,1) → b=0.625, d=0.125, u=0.25 — belief-dominant at same u. Dropping u below 0.15 requires larger effective independent evidence mass under the counting rule, not renaming "thin" to "rich."

Derivation: once (r,s) are known, the word "thin" adds no information; it only invited the wrong high-u reading if taken at face value.
```

---

### Example 3:

Input:

```
Blind metrology gate over a classification release.

Propositions (keep distinct):
- p_i: "referee link L_i equals the withheld reference code."
- q_vis: "L_i is the best match given vocabulary, prose, and embeddings only."
- q_form: "the proposed realization is formally consistent (HermiT)."

Participants and membranes:
- Referee agent: admits vocabulary annotations, chapter prose, embedding similarities. Does NOT admit the withheld reference key.
- HermiT membrane: admits TBox + proposed ABox assertions only. Does NOT admit reference key or embedding scores.
- Human / scoring process: admits the withheld reference key and the referee's published links.
- Base rates: not required for qualitative disposition; do not invent projected P(p_i) without a.

Trace (batch):
1. Referee publishes links L_1..L_n with high self-reported confidence (low stated u) — claims worded as if about p_i.
2. HermiT: CONSISTENT, 0 unsat, membrane admission OK.
3. Scoring process: rejects several L_i against the withheld key; precision drops.

Fusion topology: efficacy measurement MUST keep the reference key outside the referee and HermiT niches.

Assess boundary-relative opinions, scope, escalation, and measurement validity if the key had been visible to the referee.
```

Output:
```
Proposition: p_i (reference equality); q_vis (visible best match); q_form (formal consistency)
Verdict classes: **S + E + C + P**

Participant opinions:
- Referee on q_vis: high b, low u — licensed from vocab/prose/embeddings.
- Referee on p_i: **no admitted evidence** (key outside membrane). Low stated u on p_i is **not licensed** (C) — label/confidence collapse from q_vis onto p_i is a scope error (S).
- HermiT on q_form: high b, low u — correct for q_form.
- HermiT on p_i: **no opinion** (S). Not "discount HermiT to ~zero on p_i" — that phrasing treats a non-opinion as a discounted opinion. Out of scope.
- Scoring on p_i: low u, high b or high d per link — only membrane that admits the key.

Competence / discount:
- Trust referee on q_vis (scope IN for visible match); do not transfer that trust to p_i without the key.
- HermiT remains high-trust on q_form; issue is scope, not competence on formal logic.

Fusion:
- referee(q_vis) ⊕ hermit(q_form) is not an input to p_i. **Refuse** fusion into p_i (S). v1 has no belief-constraint step here: the right move is re-scope, not constrain conflicting masses on misaligned propositions.
- Conflict on p_i appears only between scoring rejects and any claim that still asserts p_i.

Validity / escalation:
- escalate for efficacy on p_i: **yes** — only scoring disposes p_i.
- measurement_valid with key withheld: **yes** — residual u on p_i for referee/HermiT is required (anti-co-adaptation).
- key admitted to referee niche: measurement **compromised** (evaluation-niche leak).

Confirming probe: hold visible evidence fixed; grant referee key access only. If accuracy on p_i jumps with no new domain signal, leak confirmed.
```

---

### Example 4:

Input:

```
Federated remediation loop (boundary → signal → Remediate → parse → HermiT).

Joint target often written carelessly as a single p; keep the factors distinct:
- p_auth: "chosen replacement IRI is in the pinned external authority."
- p_syn: "axiom is syntactically well-formed (parse)."
- p_con: "realization is HermiT-consistent."
- p_sem: "chosen IRI is the author's intended concept" (not disposed by this loop).

Trace:
1. Boundary emits CONTAMINATION{ref: cco:DirectiveICE, ...} — ref NOT IN authority (CCO pin 2026-04-04).  <!-- coined-ok: rejection-context; hallucinated external name -->
2. Remediate request includes live CANDIDATES from current CCO (**five IRIs**) + rules + signal.
3. Agent returns Manchester axiom using cco:ont00000965 + rationale.
4. Parse membrane: OK.
5. HermiT: consistent, 0 unsat → disposition CORRECTED.

Base rates (pinned by candidate set):
- On "this candidate among the five is the one that will prove consistent," if only uniform membership prior is available before HermiT: a ≈ 1/5 = 0.2 for each candidate-consistency proposition pre-disposition.
- a for p_auth given candidates pre-filtered by authority index: high prior that each listed candidate is in-authority (membership already filtered); residual a on p_sem is not pinned by this trace.

Partial permeability:
- Boundary: authority membership, not author intent.
- Agent: signal + candidates + rules; no fiction→fix dict.
- Parse: syntax only.
- HermiT: TBox+ABox consistency only.

Retired anti-pattern: static dict DirectiveICE → ont00000965 without candidates.  <!-- coined-ok: rejection-context -->

Recover opinions per hop with scope. Are dict path and candidate path epistemically equivalent?
```

Output:
```
Proposition: p_auth, p_syn, p_con, p_sem (distinct)
Verdict classes: **S + P + C**

Participant opinions after the successful trace:
- Boundary on "DirectiveICE ∈ authority": high d, low u. On p_auth for a replacement: near-vacuous until a candidate is chosen.  <!-- coined-ok: rejection-context -->
- Agent on p_auth for ont00000965: high b if candidates are authority-filtered (membership evidence is the candidate list). On p_sem: residual u — semantic fit under-determined. Pre-HermiT on p_con for this candidate: high u with **a ≈ 0.2** (uniform over five), not low u.
- Parse on p_syn: high b, low u. On p_auth / p_con / p_sem: **no opinion** (S).
- HermiT on p_con: high b, low u after msg 5. On p_sem: **no opinion**. On p_auth: does not add membership evidence beyond consistency of whatever IRI was asserted.

Scope (S) — not discount-to-zero:
- Parse OK is not a discounted semantic verdict; it is out of scope for p_sem and p_auth.
- HermiT CORRECTED is opinion on p_con, not on p_sem. Consumers who treat CORRECTED as proof of intent commit S.

Competence:
- Boundary CONTAMINATION: high trust on membership index.
- HermiT: high trust on p_con only.

Fusion:
- Joint operational disposition CORRECTED ≈ p_auth (from candidates) ∧ p_syn ∧ p_con. Given the proposal, these hop propositions are different coordinates — combine as a conjunction of scoped opinions, not as three votes on one p.
- Rationale text is not independent extra membership evidence (no cumulative double-count with candidate list).

Dict path vs candidate path:
- Point IRI may coincide; epistemically **not equivalent**. Candidate path grounds p_auth in live authority query; u on pre-disposition p_con reflects a≈0.2 among five. Dict path freezes a map; often mis-states low u on p_auth without live-authority signal in the trace (**u not licensed**).

Confirming probe: change CCO pin so ont00000965 vanishes; candidate path re-reasons or escalates; dict path emits stale IRI until edited.
```

---

### Example 5:

Input:

```
Fusion-provenance trap (including selection effects). Proposition p: "construct C1 deserves a rich / metrology-positive evaluation under the programme's structural-and-congruence gates."

Trace:
1. kvasir → agent: STRUCTURAL_VERDICT{label: thin, on: construct C0}.
2. Feedback synthesizer → agent: DORMANT_HINT{id: H17, text: "prefer controlled vocabularies and explicit units"} — produced from the same thin-verdict family and SchemaPile norms as msg 1 (shared upstream source S).
3. Agent revises C0 → C1 (adds units, tightens types) **under H17**.
4. kvasir → agent: STRUCTURAL_VERDICT{label: rich, on: C1}.
5. Verifier V2 (embedding congruence to chapter) emits positive congruence on C1. V2 does **not** receive kvasir messages or H17 (channel-independent).

No guarantee is given that H17's transform is orthogonal to V2's congruence measure. Controlled vocabulary and explicit units are the kind of lexical change that often raises chapter-embedding congruence.

The agent proposes to fuse (i) kvasir rich on C1, (ii) "support" from applying H17, and (iii) V2 positive, all **cumulatively**, and to report very low u on p.

Which fusion is licensed? Treat selection effects explicitly. Is low u calibrated? Confirming probes?
```

Output:
```
Proposition: p = "C1 deserves rich/metrology-positive evaluation under structural-and-congruence gates"
Verdict classes: **F + C** (first- and second-order dependence)

Participant opinions (qualitative):
- kvasir on C0: thin — recover ω from notes if present; here treat as weak structural commitment / high-u or weak-b on C0 adequacy (label collapse: do not assume high-d without counts).
- kvasir on C1: rich — higher b on structural adequacy after revision.
- H17: not an independent opinion on p; transform of shared source S (recirculation).
- V2 on C1: positive congruence — channel-independent from kvasir/H17 messages, **not therefore object-independent**.

Fusion (layered):

1. **H17 with kvasir (first-order F):** H17 shares upstream S with the thin path. Cumulative fusion of "hint support" with kvasir's structural channel **double-counts**. License: **averaging or refuse** for hint-as-evidence; H17 may be cited as the *control action* that produced C1, not as extra evidence mass.

2. **V2 with kvasir (second-order F — selection effect):** C1 was **selected/optimized under H17**, and H17's edits (units, controlled vocab) are plausibly correlated with V2's embedding-congruence measure. Independence of *channel* (V2 never saw H17) is not independence of *object* (V2 scores an artifact shaped by a signal correlated with V2). Cumulative kvasir(C1 rich) ⊕ V2(positive) is **not obviously licensed**. Default under this trace: **refuse cumulative**; at most treat V2 as a dependent/averaged signal unless orthogonality is demonstrated. Marking cumulative fusion as licensed is an answer-key error.

3. **Agent's triple cumulative + very low u:** **u not licensed** (C). Dependence violations at both layers.

Calibrated posture:
- Honest report: kvasir moved C0→C1 under H17; structural channel now rich; V2 positive is **same-artifact, selection-entangled** evidence — do not stack as independent multi-source confirmation.
- measurement_valid for "independent multi-source confirmation": **compromised** under cumulative fusion; **underdetermined** until a probe tests V2⊥H17.

Confirming probes:
1. Apply the same C0→C1 edit **without** H17 (human patch with no hint). If kvasir still rich, H17 was not independent structural evidence.
2. **Selection-effect probe:** score V2 on a control set of constructs edited toward H17-like surface form but rejected by kvasir (or random unit/vocab edits that kvasir does not reward). If V2 rises in lockstep with H17-like edits regardless of structural merit, V2 is correlated with the selection policy → cumulative fusion remains refused.
3. Orthogonal edit: change C0→C1 on a structural axis V2 is known not to score (e.g. pure key topology with no lexical change). If kvasir becomes rich and V2 does not move, partial independence for that axis is supported — still do not generalize to H17-like edits without re-testing.

Through-line: the deepest fusion-provenance failure is not shared messages; it is **shared selection** of the scored object.
```

---

### Example 6:

Input:

```
Ordering / false residual + proposition shift.

Propositions:
- p: "replacement IRI cco:ont00000965 is HermiT-consistent."
- p′: "the eventually accepted replacement IRI (whatever it is after retry) is HermiT-consistent."

Boundary / priors:
- Live candidates at t0: five IRIs including ont00000965.
- Base rate pre-disposition for "this specific candidate is consistent," uniform: a(p) = 1/5 = 0.2 unless other evidence is admitted.
- W = 2 if counts appear; none required here.

Trace with timestamps:
t0  Boundary publishes CONTAMINATION + candidates (includes ont00000965).
t1  Agent publishes proposal axiom using ont00000965 (not yet membrane-disposed).
t2  Side consumer reads the agent proposal and emits ω_side with **low u** that p holds, citing "agent chose it after contamination signal."
t3  Parse OK.
t4  HermiT returns unsat (disjointness involving the chosen class).
t5  Agent retries with a different candidate; HermiT consistent → CORRECTED.

At t2, what residual did the side consumer have? Was low u on p licensed (use a = 0.2)? After t4 vs t5, what is licensed on p vs p′?
```

Output:
```
Proposition: p (ont00000965 consistent); p′ (accepted retry IRI consistent)
Verdict classes: **S + P + C**

At t2:
- Admitted: contamination context + agent proposal. NOT admitted: parse, HermiT.
- Residual on p: unresolved formal disposition. Licensed opinion: **high u**, with pinned **a = 0.2** (uniform over five candidates) — expectation ≈ 0 + 0.2·u ≈ modest, not a low-u endorsement.
- Side consumer's low-u claim: **u not licensed** (C). It treated selection as if the formal membrane had already spoken.
- Scope: agent proposal is not an opinion on p_con; consumer invented a membrane disposition (S/P).

After t4:
- HermiT unsat → high d, low u **on p** (this IRI).
- Stale low-u belief in p remains a false residual until t4 is admitted.

After t5:
- CORRECTED licenses high b on **p′** (different candidate), not a rehabilitation of p.
- p stays high-d if ont00000965 remained unsat. Conflating p with p′ is **proposition-shift (S)** — not a discount error.

Confirming probe: require side consumers to subscribe to membrane dispositions before publishing ω on consistency; any pre-t3 opinion on p must carry high u with a = 1/|candidates|. Low u pre-disposition ⇒ misconfigured permeability (downstream niche treating proposals as certified).
```

## Tags:
- Theory of Mind
- Subjective Logic
- Boundary Topology
- Opinion States
- Trust Discounting
- Evidence Fusion
- Proposition Scope
- Label Collapse
- Metrology
- Calibration
- CAS Architectures
- Multi-Agent Systems
- Federated Verification
- Synthetic
