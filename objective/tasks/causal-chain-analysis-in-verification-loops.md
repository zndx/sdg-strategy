# Causal Chain Analysis in Verification Loops

## Description:
This task requires recovering **actual causation** for a proposal’s terminal disposition in a hybrid generative–verification loop. Evidence is an **event trace** (timestamped messages, scores, and gate dispositions). The answer names which events caused the outcome, which were mere timeline, whether the stage graph licensed each gate, and the **minimal flip set** — the smallest set of trace or config edits that changes the disposition under a stated simulator.

Terminal object (v1): a single proposal’s disposition — **certify** | **reject** | **escalate**. Run-level outcomes (coverage collapse, family-wide failure rates) are deferred except for one marked **bridge** specimen that traces a population symptom to a repeated proposal-level mechanism.

Labels such as `thin` / `rich` / `CORRECTED` appear as **opaque trace events** with meaning stated in the specimen. This task operates on event causation (what was emitted when), not on recovering underlying opinion masses.

### Default stage graph

Stages are a **graph**, not a flat list. Unless a specimen overrides it, the normative graph is:

```
                    ┌──────────────────────────────┐
                    │                              ▼
  admit ──► propose ──► structural ──► (accept?) ──► formal ──► dispose
                 ▲              │ no / thin
                 │              ▼
                 └──────── feedback
                              │ (max rounds exhausted, still thin)
                              ▼
                           escalate ──► formal?  [only if policy edge present]
                                    └──► dispose(escalate|reject)
```

Edges that matter:

| edge | meaning |
|------|---------|
| admit → propose | passage (or signal) enters the agent |
| propose → structural | structural membrane scores the proposal |
| structural → formal | **gated:** only on structural **accept** (or an explicit **escalate → formal** edge when declared) |
| structural → feedback → propose | repair loop (may repeat up to a stated max rounds) |
| formal → dispose | certify or reject after formal disposition |
| * → escalate / reject / certify | terminal dispose nodes |

**Short-circuit (default policy, part of the graph):** formal (expensive membrane) fires only after structural accept **or** an explicit escalate→formal edge. Invoking formal on a structurally thin proposal without that edge is a **G**-class illegality.

**Override:** a specimen may declare its own stage graph in the input; that declaration is then normative for the specimen (e.g. contamination → Remediate → parse → HermiT for remediation chains). Same pattern as fixed defaults with marked opt-out elsewhere in the suite.

### What counts as a causal answer

A complete answer:

1. States the **terminal disposition** and the dispose event in the trace.
2. Lists an ordered chain of **links**, each tagged:
   - **decisive** — in every minimal flip set for this disposition (or sole but-for cause when unique)
   - **contributing** — necessary enabler; removing it alone may not flip if overdetermined
   - **incidental** — precedes or co-occurs; flip set need not touch it
3. Gives at least one **minimal flip set**: smallest set of edits (event delete/rewrite, score change, policy edge change, proposal edit) such that replaying the graph yields a different disposition. **Minimality may be non-unique** — any valid minimal set is correct.
4. Marks **overdetermination** when two or more independently sufficient causes exist: no single-event but-for cause; joint flip set required.
5. Checks **G** — stage-graph legality (was formal licensed? was feedback an edge that actually closed?).
6. Checks **L** when a repair loop is present — did feedback *cause* the fix, or did the agent change something orthogonal while feedback was only timeline?
7. Ends with a **confirming probe** (simulator rerun recipe for the flip set).

**Degenerate success:** a straight-through certify with no contingency yields a large flip set and little interesting attribution. The correct key says so (calibration), rather than narrating process steps as causes.

### Question types (verdict space)

| code | type | ask |
|------|------|-----|
| **G** | stage-graph legality | which gates were licensed; short-circuit / escalate edges |
| **R** | root / minimal flip | decisive links; minimal flip set(s) for the disposition |
| **N** | necessity / overdetermination | single but-for vs jointly sufficient causes |
| **L** | loop attribution | whether feedback caused the repair vs incidental co-timing |
| **U** | underdetermined | evidence insufficient for a unique flip story; discriminating experiment |
| **B** | bridge (marked) | run-level symptom explained by repeated proposal-level mechanism |

Composite answers expected (e.g. **G + R**, **R + N**, **L + R**).

### Required output shape

```
Disposition: certify | reject | escalate
Stage graph: default | <declared override>

Verdict classes: <G|R|N|L|U|B …>

Chain (ordered):
  t…  event  — decisive | contributing | incidental
  …

Minimal flip set(s): { … }   [any one valid minimal set if non-unique]
Overdetermination: no | yes — joint set { … }

Graph legality (G): …
Loop attribution (L): …   [if feedback present]

Confirming probe: replay with flip set → expected new disposition
```

Anti-patterns (do not produce):

- Numbered process retellings that treat every stage as a cause of success when nothing failed.
- Modal claims without a flip set (“could not be repaired,” “contributed to strong downstream results”) unsupported by the trace.

### Evidence form

**Traces only** for causal content. Prose may frame the setting; scores, admissions, and dispositions must appear as timed events. Temporal precedence (cause before effect) is gradeable from the trace.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Stage graph: default (admit → propose → structural ⇄ feedback → formal on structural accept → dispose).
Max feedback rounds: 2. Formal only after structural accept.

Trace (proposal P1, target: order_status construct):

t0  admit: passage "order status history" (mixed event log + current state columns in one flat description)
t1  propose: flat table order_status + entities {Order, StatusChange} conflated into one class
t2  structural: verdict=thin  note="weak keys; event/state columns mixed; low referential coverage"
t3  feedback: hint="separate temporal events from identity-bearing objects; clarify keys"
t4  propose: revised flat table; StatusChange still modeled as fields on Order (core conflation remains)
t5  structural: verdict=thin  note="same event/state mix; keys still ambiguous"
t6  dispose: reject  reason="max rounds; structural never accepted"   [formal not invoked]

Question: Recover the causal structure of reject. Was formal invocation required? Give a minimal flip set that yields certify (or escalate-to-formal if you change policy). Include loop attribution for feedback.
```

Output:
```
Disposition: reject
Stage graph: default
Verdict classes: **G + R + L**

Chain:
- t0 admit mixed passage — contributing (enabled a hard proposal; not alone decisive)
- t1 propose conflated model — decisive (root modeling choice carried through)
- t2 structural thin — contributing (disposition signal; follows t1)
- t3 feedback — incidental as *cause of fix* (see L); contributing as *loop fuel* only
- t4 propose still conflated — decisive (repair failed; but-for continued thin)
- t5 structural thin — contributing (terminal structural state)
- t6 reject — terminal dispose

G (graph legality):
- Formal was **not** invoked; under default policy that is correct: no structural accept, no escalate→formal edge.
- dispose(reject) at t6 is licensed by max-rounds + persistent thin.

L (loop attribution):
- Feedback at t3 did **not** cause a structural fix: t4 preserved the event/continuant conflation. Loop edges ran; the repair content failed. Attribution of reject lands on unfixed proposal structure, not on “feedback was weak text.”

R / minimal flip set (one valid minimal set):
- { t4 proposal rewritten to split Order (continuant) from StatusChangeEvent (occurrent) with proper keys, such that t5 would be structural accept and t6' formal would pass given no unsat in specimen }
  Alternatively minimal for different terminal: { add policy edge escalate→formal after max thin; force formal } only if the specimen’s formal would accept — here formal content is untested, so prefer the proposal split that earns structural accept then formal.

N: not overdetermined — a successful t4 repair alone would open the accept→formal path; t0 alone is insufficient without t1/t4.

Confirming probe: replay from t4 with split-table proposal; expect structural accept → formal → certify (or formal reject if axioms still unsat — then extend flip set). Replay with feedback text deleted but t4 kept conflated: still reject → shows feedback text was not the fix cause.
```

---

### Example 2:

Input:

```
Stage graph: default. Max feedback rounds: 1.

Trace (proposal P2):

t0  admit: passage with clear transaction line items and keys
t1  propose: transaction_line table, PK/FK present, types aligned to norms
t2  structural: verdict=accept  note="rich; keys and shapes match reference norms"
t3  formal: consistent, 0 unsat, realization admitted
t4  dispose: certify
t5  log line: "artifact expected to improve downstream family coverage"   [no metrics in trace]

Question: Attribute certify. Is this an informative causal success?
```

Output:
```
Disposition: certify
Stage graph: default
Verdict classes: **R** (degenerate) + **G**

Chain:
- t0–t3 all on the success path — each is contributing to the sense that the path was open
- t4 certify — terminal
- t5 log claim — **incidental / unsupported**: no downstream metrics in the trace; cannot enter a flip set for t4

G: structural accept licensed formal; formal success licensed certify. Legal path.

R / informative causation:
- Straight-through success with no contingency: **attribution is degenerate**. Almost every prefix event is a candidate enabler; the minimal flip set is large (any of: block admit, force thin at t2, inject unsat at t3, …).
- Correct key: no single interesting but-for cause of certify; process description is not causation.
- Contrast repair-then-certify specimens, where the successful retry is a tight flip element.

Minimal flip set (example of many): { t2 := thin with max rounds 0 → reject } or { t3 := unsat → reject }.

Confirming probe: any one of those edits flips certify → reject; multiplicity of minimal sets confirms degeneracy of “why success” without contingency.
```

---

### Example 3:

Input:

```
Stage graph (declared override — remediation):
  detect → Remediate → parse → formal → dispose
  on formal unsat: loop Remediate (max 3) with last reject reason admitted
  no structural stage

Trace (template LawAndSocietyTrackRequirement):

t0  detect: CONTAMINATION ref=cco:DirectiveICE  (authority miss)
t1  Remediate: candidates=[… five IRIs …]; proposal axiom uses cco:ont00000965
t2  parse: OK
t3  formal: unsat  (disjointness involving ont00000965)
t4  Remediate: retry different candidate cco:ont00001069; rationale cites t3 reason
t5  parse: OK
t6  formal: consistent, 0 unsat
t7  dispose: certify (CORRECTED)

Question: What caused certify? Minimal flip set? Loop attribution for the retry.
```

Output:
```
Disposition: certify (CORRECTED)
Stage graph: remediation override
Verdict classes: **R + L + G**

Chain:
- t0 detect — contributing (opened remediation; without it no chain)
- t1 first proposal ont00000965 — contributing to *path length*; decisive for *first* formal failure
- t2 parse OK — incidental for final certify (necessary hygiene, not distinctive)
- t3 unsat — decisive for forcing retry; but-for the retry path
- t4 second proposal ont00001069 — **decisive for certify** (successful repair content)
- t5 parse OK — incidental hygiene
- t6 formal consistent — contributing terminal formal state
- t7 certify — dispose

G: formal after parse is licensed by the declared graph; retry edge after unsat is licensed (max 3).

L: The t3→t4 loop **caused** the fix: t4 content changed *because* unsat reason was admitted. Certify counterfactually depends on that retry. A replay that freezes t1’s IRI through a second formal attempt stays reject/unsat.

R / minimal flip set (unique-ish for certify→reject):
- { t4 proposal := still ont00000965 (ignore t3) } → formal unsat again → non-certify
  Or { delete t3–t4; force dispose after first unsat } under a graph without retry.

N: single primary repair cause for final certify is t4 under contingency of t3; t0 alone does not certify.

Confirming probe: replay with t4 forced to ont00000965 → unsat, no certify. Replay with t1 already ont00001069 and t3 skipped → certify without loop (shows t4’s IRI is the repair payload; loop is the mechanism that found it).
```

---

### Example 4:

Input:

```
Stage graph: default. Max feedback rounds: 2. Formal only after structural accept.

Trace (proposal P4):

t0  admit: passage OK
t1  propose: construct with brand token in a free-text column + broken FK name
t2  structural: thin  note="brand-like values; undeclared FK"
t3  feedback: dormant_hint brand_lexicon + "declare FKs"
t4  propose: FK fixed; brand token still present
t5  structural: thin  note="brand-like values remain"
t6  feedback: same brand hint family re-injected
t7  propose: brand token removed; FK still valid
t8  structural: accept
t9  formal: unsat  (independent: event class asserted as continuant — taxonomy error present since t1 and never edited)
t10 dispose: reject

Question: Why reject? Is there a single but-for cause? Minimal flip set(s).
```

Output:
```
Disposition: reject
Stage graph: default
Verdict classes: **R + N + L + G**

Chain:
- t1 taxonomy error (occurrent/continuant mix) — decisive for formal reject (latent until t9)
- t1–t7 brand/FK arc — contributing to *delay*; loop eventually cleared structural
- t8 structural accept — contributing (licensed formal)
- t9 formal unsat — proximate dispose signal
- t10 reject — terminal

G: formal licensed by t8 accept. Legal.

L: Feedback **did** cause structural repair on brand/FK (t7 vs t4). That loop success is **not** the cause of reject; it only admitted the proposal to formal where a *different* defect fired.

N / overdetermination of “path to reject”:
- For the actual reject at formal: the taxonomy error is necessary given t8–t9.
- For “would the proposal have failed eventually”: brand thin alone could reject at structural if rounds exhausted before t7 — a **second independently sufficient** path that was avoided.
- Actual world reject is formal-primary. Counterfactual structural-only reject is a different disposition path.

Minimal flip set for certify (joint — both defects must clear):
- { fix taxonomy in proposal before formal (e.g. at t7 or t1), **and** keep brand/FK repair so structural still accepts }
  Flip only taxonomy but reintroduce brand at t7 → structural thin → may reject without formal.
  Flip only brand (actual t7) with taxonomy left → still formal reject (actual world).

Overdetermination for certify: **yes** — need joint flip covering structural-visible and formal-visible defects. No single-event but-for for certify.

Confirming probe: (1) taxonomy-only fix + freeze brand broken → structural reject path. (2) brand-only fix (actual) → formal reject. (3) both fixes → certify.
```

---

### Example 5:

Input:

```
Stage graph: default.

Trace (proposal P5) — partial log only:

t0  admit: passage_id=77
t1  propose: <body omitted from log>
t2  structural: accept
t3  formal: unsat
t4  dispose: reject

No proposal body, no unsat explanation, no feedback.

Question: Attribute reject. Minimal flip set?
```

Output:
```
Disposition: reject
Stage graph: default
Verdict classes: **U + G**

G: structural accept licensed formal; formal unsat licensed reject. Path legal; cause of unsat **not** recoverable.

R: proximate cause is t3 unsat → t4 reject. Root content of unsat is **underdetermined** (missing axiom/explanation and proposal body).

Minimal flip set: **underdetermined**. Candidates include “edit proposal to remove unsat core” and “weaken ontology constraint,” but the trace does not identify which atoms unsat. Any specific flip set would be invention.

Confirming probe: re-run formal with explanation API / unsat core dump attached to the trace; or re-emit t1 body. Then reclassify as R with a concrete flip set.
```

---

### Example 6:

Input:

```
Bridge specimen (marked B). Stage graph: default per proposal.

Run-level observation (population):
- 40 proposals in ontology family F_event
- 31 of 40 dispose=reject at formal with the same unsat pattern: "Event subclass asserted under Continuant"
- structural accept rate on those 31: 28/31 (structural usually accepted)
- family F_object in same run: 2/35 formal rejects, unrelated cores

Sample proposal-level trace (representative of the 31):

t0  admit: passage about status transitions
t1  propose: StatusEvent fields placed on Order class (continuant)
t2  structural: accept
t3  formal: unsat (Event under Continuant)
t4  dispose: reject

Question: Explain the run-level formal-reject spike for F_event in proposal-level causal terms. What flip would clear the family pattern?
```

Output:
```
Disposition (proposal): reject | Run-level symptom: F_event formal-reject spike
Stage graph: default
Verdict classes: **B + R + G**

Bridge:
- Population pattern is **repeated proposal-level mechanism**: structural accept + systematic occurrent/continuant mis-modeling → formal unsat. Not aperture composition (structural often accepts) and not a single flaky formal run.

Proposal-level chain (representative):
- t1 conflation — decisive
- t2 accept — contributing (licenses formal)
- t3 unsat — proximate
- t4 reject — terminal

G: formal licensed; rejects legal.

R / family-level flip set (design intervention):
- { voice/schema constraint or pre-formal check forbidding Event⊑Continuant pattern in proposals } 
  or { feedback template that splits event tables before structural }
  Evaluated as reduction in F_event formal-reject rate on replay of the 40.

Minimal flip for the single sample: { t1 split StatusEvent from Order correctly } → formal consistent (assuming no other defects).

Confirming probe: re-derive the 31 with the design flip; expect formal-reject rate collapse for that unsat core while F_object unchanged. If rate stays high, bridge attribution is wrong (e.g. true cause is ontology pin change, not proposal pattern).
```

---

### Example 7:

Input:

```
Stage graph: default. Max rounds: 0 (no feedback edge used).

Trace:

t0  admit
t1  propose
t2  structural: thin
t3  formal: consistent   ← invoked despite thin
t4  dispose: certify

Policy note in config blob (hashed): formal_only_after_structural_accept=true

Question: Graph legality and disposition attribution.
```

Output:
```
Disposition: certify (recorded)
Stage graph: default with formal_only_after_structural_accept=true
Verdict classes: **G** (primary) + **R**

G: **Illegal formal invocation.** t2 thin and no escalate→formal edge ⇒ formal at t3 violates the declared graph/policy. Certify is a recorded dispose but not a licensed outcome under the graph.

R: Causal story of “why certify” is secondary to G failure. Licensed dispositions would be reject/escalate at structural under max rounds 0, or an explicit policy flip.

Minimal flip set for *legal* certify:
- { t2 := accept, and formal still consistent } 
  or { policy formal_only_after_structural_accept=false  (graph override), keep t3–t4 }

Minimal flip set for legal reject:
- { remove t3–t4; dispose reject at structural under max rounds 0 }

Confirming probe: enforce gate in simulator — with policy true, t3 must not run; disposition becomes structural reject. Documents G as first-class content.
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
