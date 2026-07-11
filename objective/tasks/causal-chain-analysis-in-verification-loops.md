# Causal Chain Analysis in Verification Loops

## Description:
This task requires recovering **actual causation** for a proposal’s terminal disposition in a hybrid generative–verification loop. Evidence is an **event trace** (timestamped messages, scores, and gate dispositions). The answer names which events caused the outcome, which were mere timeline, whether the stage graph licensed each gate, and the **minimal flip set** — the smallest set of **exogenous** edits that changes the disposition under the stated replay semantics.

Terminal object (v1): a single proposal’s disposition — **certify** | **reject** | **escalate**. Run-level outcomes are deferred except for one marked **aggregate** specimen (**A**) that traces a population symptom to a repeated proposal-level mechanism.

Labels such as `thin` / `rich` / `CORRECTED` appear as **opaque trace events** with meaning stated in the specimen. This task operates on event causation (what was emitted when). For recovering epistemic content of those labels as opinions, see the separate opinion-states task card; it is out of scope here.

### Default stage graph

Stages are a **graph**. Unless a specimen overrides it, the normative graph is:

```mermaid
flowchart TD
  admit([admit]) --> propose[propose]
  propose --> structural[structural]
  structural -->|accept| formal[formal]
  structural -->|thin, rounds remain| feedback[feedback]
  structural -->|thin, max rounds exhausted| dispose_struct[dispose: reject or escalate]
  feedback -->|repair| propose
  structural -->|escalate policy edge| formal
  formal --> dispose[dispose: certify or reject]
```

| edge | meaning |
|------|---------|
| admit → propose | passage or signal enters the agent |
| propose → structural | structural membrane scores the proposal |
| structural → formal | **gated:** structural **accept**, or an explicit **escalate-policy** edge on the structural node |
| structural → feedback → propose | repair loop while rounds remain |
| structural → dispose | max rounds exhausted while still thin (no formal) |
| formal → dispose | certify or reject after formal disposition |

**Short-circuit (default):** formal fires only after structural accept **or** an explicit structural→formal escalate-policy edge. Invoking formal on a structurally thin proposal without that edge is a **G**-class illegality.

**Escalate** is a **terminal disposition** value (alongside certify / reject), not a routing node. Routing to formal under special policy is the **escalate-policy edge**, not a hop through an escalate stage.

**Override:** a specimen may declare its own stage graph; that declaration is normative for the specimen (e.g. contamination → Remediate → parse → HermiT).

### Replay semantics (v1 constant)

Ground truth is defined by a **frozen-suffix / exogenous–derived partition**:

| class | events | on replay |
|-------|--------|-----------|
| **Exogenous** (agent- or operator-emitted) | admit content, proposal bodies, feedback/hint text, Remediate proposals, policy/config pins | **Editable** in a flip set; if not edited, **frozen as recorded** |
| **Derived** (mechanical stages) | structural verdicts, parse results, formal dispositions, dispose | **Always recomputed** from current exogenous state and the stage graph; **not** directly editable in a flip set |

Consequences:

1. Flip sets may touch only **exogenous** material (and design/config — see below). Writing `{ t2 := thin }` when t2 is structural is illegal under v1.
2. **Flip sets are event-granular:** one edit to an exogenous event is one flip-set element, even when that edit repairs several defects in the body. **Overdetermination (N) is defect-granular:** a defect is independently sufficient iff repairing *that defect alone* (leaving other defects in place) leaves the disposition value unchanged. Event-cardinality of a minimal flip set and defect-level N can therefore diverge (one edited event, two sufficient defects).
3. **Decisive** (event-level): the exogenous event appears in **every** minimal flip set that changes the actual **disposition value**, under frozen-suffix replay.
4. Earlier proposals superseded by a later frozen proposal are typically **contributing** (path history); the **last exogenous proposal body** that feeds the terminal derived path is the usual decisive locus for proposal defects.
5. Minimality is non-unique; any valid minimal exogenous flip set is correct.

**Frozen-suffix corners (required for complete replay):**

1. If derived recomputation **requires an exogenous event that is absent** from the edited trace (e.g. a third Remediate after a forced re-unsat, when no further Remediate was recorded), the chain **disposes by exhaustion** at that point per the stage graph (reject / escalate as the graph specifies). No agent events are invented.
2. If derived recomputation **terminates before** later recorded timestamps would be consumed (e.g. first formal already consistent), those later recorded exogenous and derived events are **dropped** (orphaned suffix).

**Disposition value:** a **flip** is a change of terminal disposition **value** among {certify, reject, escalate}. An edit that only relocates the failing stage (e.g. reject-at-formal → reject-at-structural) keeps value `reject` and is a **non-flip**; it may still be reported in probes as a path change.

### Trace flips vs design flips

| kind | scope | reported as |
|------|--------|-------------|
| **Trace flip** | edits to exogenous events in the recorded trace (admit, propose bodies, hints) | **Minimal flip set** — used for decisive/contributing tags |
| **Design flip** | config/policy/ontology-pin/voice changes outside a single proposal body | **Design flip** field — legal confirming material; **does not** strip decisive tags from trace events when an alternate design path also flips |

Decisive/contributing tags are computed over **trace-edit scope**. Design flips may appear in confirming probes and aggregate interventions without redefining those tags.

### What counts as a causal answer

1. Terminal disposition and dispose event.
2. Ordered chain: exogenous events tagged **decisive** | **contributing** | **incidental**; mechanical events tagged **derived** (optional subordinate note). Causal tags apply to exogenous events; derived events carry the **derived** marker and are never flip-set elements.
3. At least one **minimal flip set** of exogenous **event** edits that change disposition **value** (non-unique OK).
4. **Overdetermination (N)** at **defect** grain when two or more independently sufficient defects remain active on the actual terminal path — repairing either defect alone leaves the same disposition value. (A defect repaired in-flight is inactive.)
5. **G** — stage-graph legality.
6. **L** — when a repair loop is present: did feedback cause the repair content?
7. **Confirming probe** — simulator recipe (flips, non-flips, design flips as needed).

**Gated-topology theorem (for N):** under the default graph, a structural-visible defect and a formal-visible defect cannot **co-cause** a *formal* reject, because formal never runs while structural is thin. True defect-level overdetermination at formal requires **two independent formal-visible defects** (e.g. two unsat cores) in the proposal that reached formal.

**Degenerate success:** straight-through certify without contingency yields many exogenous minimal flips and little informative attribution — state that explicitly.

### Question types (verdict space)

| code | type | ask |
|------|------|-----|
| **G** | stage-graph legality | which gates were licensed; short-circuit / escalate-policy edges |
| **R** | root / minimal flip | decisive exogenous links; minimal flip set(s) |
| **N** | necessity / overdetermination | single but-for vs jointly sufficient active causes |
| **L** | loop attribution | whether feedback caused the repair |
| **U** | underdetermined | evidence insufficient; discriminating experiment |
| **A** | aggregate (marked) | run-level symptom from repeated proposal-level mechanism |

### Required output shape

```
Disposition: certify | reject | escalate
Stage graph: default | <declared override>
Replay: frozen-suffix (exogenous frozen unless edited; derived recomputed)

Verdict classes: <G|R|N|L|U|A …>

Chain (ordered):
  t…  exogenous event  — decisive | contributing | incidental
  t…  mechanical event — derived
  …

Minimal flip set(s) [exogenous events only; event-granular]: { … }
Design flip(s) [optional]: { … }
Overdetermination (defect-granular): no | yes — defects { … }

Graph legality (G): …
Loop attribution (L): …   [if feedback present]

Confirming probe: replay with flip set → expected new disposition
```

Anti-patterns:

- Process retellings of frictionless success as a unique causal chain.
- Modal claims without an exogenous flip set (“could not be repaired,” “strong downstream results”) when the trace lacks support.
- Editing derived events inside a flip set.

### Evidence form

**Traces only** for causal content. Prose may frame; scores and dispositions appear as timed events.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Stage graph: default. Max feedback rounds: 2. Formal only after structural accept.
Replay: frozen-suffix (v1).

Trace (proposal P1, target: order_status construct):

t0  admit: passage "order status history" (mixed event log + current state in one flat description)
t1  propose: flat table order_status; Order and StatusChange conflated into one class
t2  structural: verdict=thin  note="weak keys; event/state mixed; low referential coverage"   [derived]
t3  feedback: hint="separate temporal events from identity-bearing objects; clarify keys"
t4  propose: revised flat table; StatusChange still fields on Order (core conflation remains)
t5  structural: verdict=thin  note="same event/state mix"   [derived]
t6  dispose: reject  reason="max rounds exhausted; still thin"   [derived; formal not invoked]

Simulator fact: a proposal body that cleanly splits Order (continuant) from StatusChangeEvent (occurrent) with proper keys is **formally consistent** (0 unsat) under this pin.

Question: Causal structure of reject. Formal required? Minimal flip set for a different disposition. Loop attribution.
```

Output:
```
Disposition: reject
Stage graph: default
Replay: frozen-suffix
Verdict classes: **G + R + L**

Chain:
- t0 admit mixed passage — contributing
- t1 first conflated propose — contributing (superseded under frozen-suffix by t4)
- t2 structural thin — **derived**
- t3 feedback — incidental as cause of fix (L)
- t4 propose still conflated — **decisive**
- t5 structural thin — **derived**
- t6 reject — **derived** terminal

G: formal omitted correctly. dispose(reject) licensed by max-rounds + thin (structural → dispose).

L: t3 did not produce a structural fix; t4 kept the conflation.

R / minimal flip set (exogenous event-granular; one valid set):
- { t4 := split Order / StatusChangeEvent body }
  Replay: t5 accept → formal consistent (simulator fact) → **certify** (disposition value flips reject → certify).
  { t1 := split … } alone does **not** flip: t4 stays frozen-conflated → still reject. t1 contributing, t4 decisive.

Design flip (optional): escalate-policy edge after max thin — separate field; does not redefine t4’s decisive tag.

N: defect-level overdetermination no for actual reject.

Confirming probe: edit only t4 → certify. Edit only t1, freeze t4 → reject. Delete t3, keep t4 → reject.
```

---

### Example 2:

Input:

```
Stage graph: default. Max feedback rounds: 1. Replay: frozen-suffix.

Trace (proposal P2):

t0  admit: passage with clear transaction line items and keys
t1  propose: transaction_line table, PK/FK present, types aligned to norms
t2  structural: verdict=accept  note="rich; keys and shapes match"   [derived]
t3  formal: consistent, 0 unsat   [derived]
t4  dispose: certify   [derived]
t5  log: "artifact expected to improve downstream family coverage"   [no metrics]

Question: Attribute certify. Informative causal success?
```

Output:
```
Disposition: certify
Stage graph: default
Replay: frozen-suffix
Verdict classes: **R** (degenerate) + **G**

Chain:
- t0, t1 — contributing
- t2 structural accept — **derived**
- t3 formal consistent — **derived**
- t4 certify — **derived**
- t5 log — incidental (no metrics)

G: accept licensed formal; formal licensed certify.

R: **Degenerate success.** Many size-1 exogenous event flips change disposition value; none is uniquely informative.

Minimal flip set examples (exogenous; any one valid):
- { t0 := off-domain admit that cannot support the proposal } → reject (value flip)
- { t1 := corrupt proposal body } → thin → reject under max rounds (value flip)
- Design flip: { ontology pin making t1 axioms unsat } → formal reject after accept (value flip)

Illegal under v1: { t2 := thin }, { t3 := unsat } — derived edits.

Confirming probe: any exogenous flip above → disposition value leaves certify. Multiplicity calibrates degeneracy.
```

---

### Example 3:

Input:

```
Stage graph (override — remediation):
  detect → Remediate → parse → formal → dispose
  on formal unsat: loop Remediate (max 3) with last reject reason admitted to the next Remediate
Replay: frozen-suffix (Remediate proposals exogenous; parse/formal/dispose derived).

Trace:

t0  detect: CONTAMINATION ref=cco:DirectiveICE
t1  Remediate: candidates=[five IRIs]; axiom uses cco:ont00000965
t2  parse: OK   [derived]
t3  formal: unsat (disjointness involving ont00000965)   [derived]
t4  Remediate: retry cco:ont00001069; rationale cites t3 reason
t5  parse: OK   [derived]
t6  formal: consistent, 0 unsat   [derived]
t7  dispose: certify (CORRECTED)   [derived]

Question: What caused certify? Minimal flip set? Loop attribution. (Design flips optional.)
```

Output:
```
Disposition: certify (CORRECTED)
Stage graph: remediation override
Replay: frozen-suffix
Verdict classes: **R + L + G**

Chain:
- t0 detect — contributing
- t1 first Remediate ont00000965 — contributing (superseded for final certify by t4)
- t2 parse OK — **derived**
- t3 unsat — **derived**
- t4 Remediate ont00001069 — **decisive** (repair payload)
- t5 parse OK — **derived**
- t6 formal consistent — **derived**
- t7 certify — **derived**

G: parse→formal and unsat→Remediate retry licensed by override.

L: loop is the **mechanism**; t4’s IRI is the **repair payload**.

R / minimal flip set (exogenous event-granular):
- { t4 := still ont00000965 }
  Replay: t5–t6 recompute → formal unsat. Graph requests another Remediate; **no further exogenous Remediate exists in the edited trace** → dispose by exhaustion → **reject** (disposition value flips certify → reject). Orphan rule does not apply here (chain continues until stuck).

Alternate illustrating corner (ii):
- { t1 := already ont00001069 } (t4 left as recorded)
  Replay: first formal consistent → dispose **certify**; recorded t4/t5/t6 are **dropped** as orphaned suffix.

Design flip (separate field): ontology pin removing the disjointness — may certify with t4 frozen to ont00000965; does not strip t4’s decisive tag under trace-scope.

Confirming probe: t4 rollback → exhaust → reject. t1 correct IRI → early certify, suffix dropped (payload vs mechanism).
```

---

### Example 4:

Input:

```
Stage graph: default. Max feedback rounds: 2. Replay: frozen-suffix.

Trace (proposal P4) — repaired structural defect + latent formal defect:

t0  admit: passage OK
t1  propose: brand token in free-text column + broken FK + Event-as-continuant taxonomy error
t2  structural: thin  note="brand-like values; undeclared FK"   [derived]
t3  feedback: brand_lexicon + "declare FKs"
t4  propose: FK fixed; brand remains; taxonomy error remains
t5  structural: thin  note="brand-like values remain"   [derived]
t6  feedback: brand hint again
t7  propose: brand removed; FK valid; taxonomy error **still present** (unchanged since t1)
t8  structural: accept   [derived]
t9  formal: unsat  note="Event asserted under Continuant"   [derived]
t10 dispose: reject   [derived]

Question: Why reject? Single but-for? Minimal flip set for certify.
```

Output:
```
Disposition: reject
Stage graph: default
Replay: frozen-suffix
Verdict classes: **R + N + L + G**

Chain:
- t1 taxonomy introduced — contributing history (still in t7)
- t1–t6 brand/FK arc — contributing to **delay** only
- t7 propose (brand clean, taxonomy wrong) — **decisive**
- t8 accept — **derived**
- t9 unsat — **derived**
- t10 reject — **derived**

G: formal licensed by t8.

L: Feedback caused brand/FK repair; that loop is not the cause of reject.

N: Actual disposition value is **reject** (formal). Brand defect inactive (repaired in-flight). Sole active formal defect = taxonomy in t7. Defect-level overdetermination: **no**. (Gated-topology theorem: structural- and formal-visible defects cannot co-cause a formal reject.)

Minimal flip set for certify (event-granular, size 1):
- { t7 := brand/FK-clean body **with taxonomy corrected** }
  Replay → accept → formal consistent → **certify** (value flip).

Confirming probe: taxonomy fix at t7 → certify. Reintroduce brand at t7 with taxonomy fixed → structural thin → **reject** — same disposition **value**, different stage (path change / **non-flip**); reportable in probes, not counted as a flip.
```

---

### Example 5:

Input:

```
Stage graph: default. Replay: frozen-suffix.

Trace (proposal P5) — true formal overdetermination (two unsat cores):

t0  admit: passage OK
t1  propose: body contains BOTH
      (core A) Event subclass asserted under Continuant
      (core B) unsatisfiable cardinality: min 2 on a property forced empty by disjoint axioms
t2  structural: accept   [derived — neither core is structural-visible]
t3  formal: unsat  cores={A, B}  (explanation lists both independently)   [derived]
t4  dispose: reject   [derived]

Known simulator fact: repairing only A leaves unsat(B); repairing only B leaves unsat(A); repairing both → consistent.

Question: But-for structure of reject. Minimal flip set for certify.
```

Output:
```
Disposition: reject
Stage graph: default
Replay: frozen-suffix
Verdict classes: **R + N + G**

Chain:
- t1 proposal containing cores A and B — **decisive** (event-level: sole exogenous body in every minimal flip set)
- t2 accept — **derived**
- t3 unsat {A,B} — **derived**
- t4 reject — **derived**

G: formal licensed.

N (defect-granular): **yes.** Core A alone is independently sufficient for reject; core B alone is independently sufficient. Repairing only A leaves reject; repairing only B leaves reject.

R / minimal flip set (event-granular):
- { t1 := body with **both** cores repaired }
  Event-cardinality **1** (one exogenous edit). That single edit must clear both defects; partial repairs of t1 that leave one core are still the event t1 edited, but they **fail to flip** disposition value → they are not members of any *successful* minimal flip set.

Confirming probe: t1 edit clearing only A → still reject (value unchanged). Only B → still reject. Both → certify (value flip). Aligns event-granular flips with defect-granular N.
```

---

### Example 6:

Input:

```
Stage graph: default. Replay: frozen-suffix.

Trace (proposal P6) — partial log:

t0  admit: passage_id=77
t1  propose: <body omitted>
t2  structural: accept   [derived]
t3  formal: unsat   [derived; no core dump]
t4  dispose: reject   [derived]

Question: Attribute reject. Minimal flip set?
```

Output:
```
Disposition: reject
Stage graph: default
Replay: frozen-suffix
Verdict classes: **U + G**

G: path legal (accept → formal → reject).

R: t2–t4 **derived**. Root exogenous content of unsat **underdetermined** (t1 body and cores missing).

Minimal flip set: **underdetermined**. Naming a specific t1 edit invents atoms.

Confirming probe: attach t1 body + unsat cores; reclassify under R/N with an event-granular flip set.
```

---

### Example 7:

Input:

```
Aggregate specimen (marked A). Stage graph: default per proposal. Replay: frozen-suffix.

Run-level observation:
- 40 proposals in family F_event
- 31/40 dispose=reject at formal; same unsat pattern "Event subclass under Continuant"
- structural accept on 28/31 of those
- F_object in same run: 2/35 formal rejects, unrelated cores

Representative proposal trace:

t0  admit: status transitions passage
t1  propose: StatusEvent fields on Order (continuant)
t2  structural: accept   [derived]
t3  formal: unsat (Event under Continuant)   [derived]
t4  dispose: reject   [derived]

Question: Explain the F_event spike in proposal-level terms. Trace flip vs design flip.
```

Output:
```
Disposition (sample): reject | Run-level: F_event formal-reject spike
Stage graph: default
Replay: frozen-suffix
Verdict classes: **A + R + G**

A (aggregate):
- Population pattern = **repeated proposal-level mechanism**: structural accept + systematic occurrent/continuant mis-model → formal unsat.
- High structural-accept rate on the failing set weighs against aperture-composition as primary account.

Sample chain:
- t1 conflation — **decisive**
- t2 accept — **derived**
- t3 unsat — **derived**
- t4 reject — **derived**

G: formal licensed.

Minimal flip set (sample):
- { t1 := StatusEvent split from Order correctly } → certify (simulator: split body consistent)

Design flip (family-level; separate field):
- { voice or pre-formal check forbidding Event⊑Continuant }
  Does not redefine t1’s decisive tag on the sample.

Confirming probe: design flip on the 31 → expect F_event formal-reject rate collapse with **F_object stable**. If F_event rate stays high under the design flip, A-attribution to the proposal pattern is **falsified** (rival causes: ontology pin change, shared formal config, etc. — not discriminated by F_object alone). Sample-level: exogenous t1 fix → certify.
```

---

### Example 8:

Input:

```
Stage graph: default. Max rounds: 0 (feedback unused). Replay: frozen-suffix.
Policy (config, hashed): formal_only_after_structural_accept=true

Trace:

t0  admit: ...
t1  propose: body B
t2  structural: thin   [derived]
t3  formal: consistent   [derived — invoked despite thin]
t4  dispose: certify   [derived]

Question: Graph legality and disposition attribution.
```

Output:
```
Disposition: certify (recorded)
Stage graph: default; formal_only_after_structural_accept=true
Replay: frozen-suffix
Verdict classes: **G** (primary) + **R**

G: **Illegal formal invocation.** t2 thin and no escalate-policy edge ⇒ t3 violates the graph. Recorded certify is unlicensed under the declared policy.

R: Attribution of “why certify” is secondary to G. Enforcing the gate yields structural **reject** (max rounds 0) — disposition **value** flips certify → reject.

Minimal flip set for *licensed* certify:
- Trace: { t1 := body that derives structural accept } (formal consistent) → licensed certify path
- Design: { formal_only_after_structural_accept := false } — design flip field

Illegal: { t2 := accept } — derived edit.

Confirming probe: enforce policy → formal does not run → dispose reject. Documents G.
```

## Tags:
- Causal Chain Analysis
- Causal Reasoning
- Verification and Validation
- Hybrid Generative-Verification Pipelines
- Stage Graphs
- Counterfactual Reasoning
- Feedback Loops
- Formal Methods
- Systems Thinking
- Synthetic
